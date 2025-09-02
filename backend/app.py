from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    with app.app_context():
        from routes import main
        app.register_blueprint(main)
        db.create_all()  # Create database tables if they don't exist

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
