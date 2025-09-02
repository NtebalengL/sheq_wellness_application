# app.py
import os, hashlib, jwt, re
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pathlib import Path
from typing import Optional

from db import Base, User, Message, Alert, SessionLocal, init_db
from models import AskRequest, AskResponse, ResourceItem, AuthRequest, TokenResponse

# --- Load environment variables ---
from dotenv import load_dotenv
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET", "change_this_secret")
DATA_RETENTION_DAYS = int(os.getenv("DATA_RETENTION_DAYS", "365"))

# --- Password hashing ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Initialize FastAPI ---
app = FastAPI(title="SHEQ+ Backend", version="0.2.0")

# --- Allow CORS ---
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Initialize database ---
init_db()

# --- Dependency for DB session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Authentication helpers ---
def hash_user(identifier: str):
    return hashlib.sha256((identifier or "anonymous").encode()).hexdigest()

def create_user(db: Session, username: str, password: str, is_admin: bool = False):
    pwd = pwd_context.hash(password)
    user = User(username=username, password_hash=pwd, is_admin=is_admin)
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        return None

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.password_hash):
        return user
    return None

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=4)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm="HS256")

def get_current_user(Authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not Authorization:
        raise HTTPException(status_code=401, detail="Missing auth")
    try:
        scheme, token = Authorization.split()
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(User).filter(User.username == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Safety keywords ---
SAFETY_KEYWORDS = ["rape", "assault", "abuse", "suicide", "harm myself", "forced", "sexual violence", "molest", "incest"]

# -------------------
# HEALTH CHECK
# -------------------
@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    count = db.query(Message).count()
    return {"status": "ok", "messages": count}

# -------------------
# AUTHENTICATION
# -------------------
@app.post("/api/auth", response_model=TokenResponse)
def auth(req: AuthRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, req.username, req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}

# -------------------
# ASK / FAQ
# -------------------
FAQ_PATH = Path(__file__).parent / "content" / "faq.yaml"

def load_faq(path=FAQ_PATH):
    items = []
    if not path.exists():
        return items
    with open(path, "r", encoding="utf-8") as f:
        q = None; a = None
        for line in f:
            line = line.strip()
            if line.startswith("- q:"):
                if q and a:
                    items.append({"q": q, "a": a})
                q = line.split(":", 1)[1].strip()
                a = None
            elif line.startswith("a:"):
                a = line.split(":", 1)[1].strip()
        if q and a:
            items.append({"q": q, "a": a})
    return items

FAQ_ITEMS = load_faq()
QUESTIONS = [it["q"] for it in FAQ_ITEMS]
ANSWERS = [it["a"] for it in FAQ_ITEMS]

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(QUESTIONS) if QUESTIONS else None

@app.post("/api/ask", response_model=AskResponse)
def ask(req: AskRequest, db: Session = Depends(get_db)):
    text = req.text.strip()
    if len(text) < 3:
        raise HTTPException(status_code=400, detail="Question too short.")
    if X is None:
        answer = "Knowledge base updating. Visit a clinic or hotline."
        confidence = 0.0
    else:
        q_vec = vectorizer.transform([text])
        sims = cosine_similarity(q_vec, X).flatten()
        best_idx = int(sims.argmax())
        confidence = float(sims[best_idx])
        answer = ANSWERS[best_idx]

    answer_out = answer + "\n\nNote: This is general info, not medical advice."

    flagged = any(re.search(r"\b" + re.escape(kw) + r"\b", text, flags=re.IGNORECASE) for kw in SAFETY_KEYWORDS)

    try:
        uid = hash_user(req.user_id or "")
        msg = Message(user_hash=uid, channel=req.channel or "web", text=text, response=answer_out, flagged=flagged)
        db.add(msg)
        db.commit()
        db.refresh(msg)
        if flagged:
            alert = Alert(message_id=msg.id, reason="safety_keyword")
            db.add(alert)
            db.commit()
    except Exception:
        db.rollback()

    return AskResponse(answer=answer_out, source="faq", confidence=round(confidence,3), escalate=flagged)

# -------------------
# RESOURCES
# -------------------
@app.get("/api/resources")
def resources():
    items = [
        {"name": "SA Emergency", "type": "emergency", "phone": "10111", "notes": "Immediate danger"},
        {"name": "GBV Command Centre", "type": "hotline", "phone": "0800 428 428", "notes": "24/7 support"},
        {"name": "Childline South Africa", "type": "hotline", "phone": "116", "notes": "Free from most networks"},
        {"name": "SRH Clinic Finder", "type": "web", "url": "https://www.health.gov.za/", "notes": "Find local services"},
    ]
    return {"resources": items}

# -------------------
# ADMIN ENDPOINTS
# -------------------
@app.get("/api/admin/analytics")
def analytics(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    total = db.query(Message).count()
    flagged = db.query(Message).filter(Message.flagged==True).count()
    alerts = db.query(Alert).count()
    recent = db.query(Message).order_by(Message.created_at.desc()).limit(10).all()
    recent_list = [{"id": m.id, "text_preview": m.text[:120]+"..." if len(m.text)>120 else m.text, "flagged": m.flagged, "created_at": m.created_at.isoformat()} for m in recent]
    return {"total_messages": total, "flagged_messages": flagged, "alerts": alerts, "recent": recent_list}

@app.post("/api/admin/create_user")
def create_user_endpoint(req: AuthRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    u = create_user(db, req.username, req.password, is_admin=False)
    if not u:
        raise HTTPException(status_code=400, detail="Could not create user (exists?)")
    return {"created": req.username}

@app.post("/api/admin/cleanup")
def cleanup(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    cutoff = datetime.utcnow() - timedelta(days=DATA_RETENTION_DAYS)
    deleted = db.query(Message).filter(Message.created_at < cutoff).delete()
    db.commit()
    return {"deleted": deleted}
