#!/usr/bin/env python3
"""
MNPS v2 - Database Setup Script
Creates initial admin user and demo data
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from models import Base, User, StudentResult, Broadcast

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def setup_database():
    """Setup the database with initial data."""
    
    # Database URL
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./mnps_v2.db")
    
    # Create engine and session
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        
        if not admin_user:
            # Create admin user
            admin_user = User(
                username="admin",
                email="admin@mayowaschool.edu.ng",
                password_hash=pwd_context.hash("admin123"),
                role="admin",
                full_name="System Administrator",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(admin_user)
            print("✅ Admin user created")
        else:
            print("ℹ️  Admin user already exists")
        
        # Create demo student user
        student_user = db.query(User).filter(User.username == "student001").first()
        
        if not student_user:
            student_user = User(
                username="student001",
                email="student001@mayowaschool.edu.ng",
                password_hash=pwd_context.hash("student123"),
                role="student",
                full_name="John Doe",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(student_user)
            print("✅ Demo student user created")
        else:
            print("ℹ️  Demo student user already exists")
        
        # Create demo teacher user
        teacher_user = db.query(User).filter(User.username == "teacher001").first()
        
        if not teacher_user:
            teacher_user = User(
                username="teacher001",
                email="teacher001@mayowaschool.edu.ng",
                password_hash=pwd_context.hash("teacher123"),
                role="teacher",
                full_name="Jane Smith",
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(teacher_user)
            print("✅ Demo teacher user created")
        else:
            print("ℹ️  Demo teacher user already exists")
        
        # Create demo results
        existing_results = db.query(StudentResult).filter(StudentResult.student_id == "student001").count()
        
        if existing_results == 0:
            # Create sample results
            sample_results = [
                StudentResult(
                    student_id="student001",
                    student_name="John Doe",
                    class_name="Primary 5",
                    session="2024/2025",
                    term="1st Term",
                    subjects='{"Mathematics": 85, "English": 78, "Science": 92, "Social Studies": 80, "Art": 88}',
                    total_score=423,
                    average_score=84.6,
                    grade="A",
                    position="3rd",
                    remarks="Excellent performance. Keep up the good work!",
                    created_at=datetime.utcnow()
                ),
                StudentResult(
                    student_id="student001",
                    student_name="John Doe",
                    class_name="Primary 5",
                    session="2024/2025",
                    term="2nd Term",
                    subjects='{"Mathematics": 88, "English": 82, "Science": 90, "Social Studies": 85, "Art": 90}',
                    total_score=435,
                    average_score=87.0,
                    grade="A",
                    position="2nd",
                    remarks="Outstanding improvement! Well done!",
                    created_at=datetime.utcnow()
                ),
            ]
            
            for result in sample_results:
                db.add(result)
            
            print("✅ Demo results created")
        else:
            print("ℹ️  Demo results already exist")
        
        # Create demo broadcasts
        existing_broadcasts = db.query(Broadcast).count()
        
        if existing_broadcasts == 0:
            sample_broadcasts = [
                Broadcast(
                    title="Welcome to New Academic Session",
                    message="Welcome to the 2024/2025 academic session. We are excited to have you back and look forward to a successful year ahead.",
                    priority="normal",
                    target_audience="all",
                    is_active=True,
                    created_at=datetime.utcnow()
                ),
                Broadcast(
                    title="Parent-Teacher Meeting",
                    message="Parent-Teacher meeting is scheduled for next Friday. Please ensure you attend to discuss your child's progress.",
                    priority="high",
                    target_audience="parents",
                    is_active=True,
                    created_at=datetime.utcnow()
                ),
            ]
            
            for broadcast in sample_broadcasts:
                db.add(broadcast)
            
            print("✅ Demo broadcasts created")
        else:
            print("ℹ️  Demo broadcasts already exist")
        
        # Commit all changes
        db.commit()
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 Demo Credentials:")
        print("Admin: username=admin, password=admin123")
        print("Student: username=student001, password=student123")
        print("Teacher: username=teacher001, password=teacher123")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    setup_database()
