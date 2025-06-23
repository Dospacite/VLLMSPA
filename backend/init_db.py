#!/usr/bin/env python3
"""
Database initialization script for VLLMSPA backend.
This script creates the database tables and initial migration.
"""

from app import create_app, db
from app.models import User, Message

def init_db():
    """Initialize the database with all models."""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # You can add some initial data here if needed
        # For example, create a test user:
        # test_user = User(username='testuser')
        # test_user.set_password('password123')
        # db.session.add(test_user)
        # db.session.commit()
        # print("Test user created!")

if __name__ == '__main__':
    init_db() 