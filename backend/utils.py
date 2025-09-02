import requests
from flask_mail import Message
from app import mail

# Simple AI using DuckDuckGo Instant Answer API (can replace with OpenAI API)
def fetch_ai_response(query):
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json"}
    res = requests.get(url, params=params).json()
    answer = res.get("AbstractText") or "I couldn't find an answer. Please try rephrasing your question."
    return answer

def send_email(subject, body, to="admin@sheq.com"):
    msg = Message(subject, sender="noreply@sheq.com", recipients=[to])
    msg.body = body
    mail.send(msg)
