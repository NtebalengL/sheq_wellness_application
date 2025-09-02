from flask import Blueprint, request, jsonify
from app import db, bcrypt, mail
from models import User, Report
from utils import fetch_ai_response, send_email
from flask_mail import Message

main = Blueprint('main', __name__)

@main.route("/api/register", methods=["POST"])
def register():
    data = request.json
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'], password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@main.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful", "is_admin": user.is_admin})
    return jsonify({"error": "Invalid credentials"}), 401

@main.route("/api/report", methods=["POST"])
def report():
    data = request.json
    new_report = Report(category=data["category"], description=data["description"], contact_info=data.get("contact_info"))
    db.session.add(new_report)
    db.session.commit()
    send_email(subject="New Abuse Report", body=f"{data}")
    return jsonify({"message": "Report submitted"}), 201

@main.route("/api/ai", methods=["POST"])
def ai_bot():
    query = request.json.get("query")
    answer = fetch_ai_response(query)
    return jsonify({"response": answer})
