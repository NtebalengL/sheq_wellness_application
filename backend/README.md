# SHEQ+ Backend (FastAPI) - Upgraded MVP

Includes:
- Anonymous Q&A endpoint using TF-IDF similarity over a curated, reviewed SRH FAQ.
- Safety rails: crisis keyword detection and automatic escalation card responses.
- Authentication (JWT) for NGO/admin users to view analytics dashboard.
- Privacy-first logging: user identifiers hashed; configurable data retention.
- Aggregated analytics endpoints for dashboards (no PII returned).

Quickstart (Windows PowerShell):
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
cp .env.sample .env
uvicorn app:app --reload --port 8000
```

Then serve the frontend (simple static server):
```powershell
cd ../frontend
python -m http.server 5173
```

Open http://localhost:5173 for the app and http://localhost:5173/admin.html for the admin dashboard (login required).
