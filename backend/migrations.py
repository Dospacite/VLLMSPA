from app import create_app, db
from app.models import User, Message

def init_db():
    """Initialize the database with tables"""
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

def drop_db():
    """Drop all tables (use with caution!)"""
    app = create_app()
    with app.app_context():
        db.drop_all()
        print("All tables dropped!")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        drop_db()
    else:
        init_db() 