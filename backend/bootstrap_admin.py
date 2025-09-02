# bootstrap_admin.py
# Run once to create an initial admin user.
# Usage: python bootstrap_admin.py username password

import sys
from db import SessionLocal, init_db
from app import create_user as cu

def main():
    if len(sys.argv) < 3:
        print("Usage: python bootstrap_admin.py username password")
        return

    username = sys.argv[1]
    password = sys.argv[2]

    # Initialize database and tables
    try:
        init_db()
        print("Database initialized successfully.")
    except Exception as e:
        print("Error initializing database:", e)
        return

    # Create a new session
    db = SessionLocal()
    try:
        user = cu(db, username, password, is_admin=True)
        if user:
            print(f"Created admin user: {username}")
        else:
            print(f"Admin user '{username}' already exists or could not be created.")
    except Exception as e:
        print("Error creating admin user:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()
