from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, create_tables
from models import User, StudentResult, Broadcast
from auth import create_access_token, verify_token, get_password_hash, verify_password
from schemas import UserCreate, UserLogin, StudentResultCreate, BroadcastCreate
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Create database tables
create_tables()

app = FastAPI(
    title="MNPS v2 - School Management API",
    description="Simple, reliable school management system",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "MNPS v2 - School Management API",
        "school": "Mayowa Nursery & Primary School",
        "address": "Oda Road, Akure, Ondo State, Nigeria",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": time.time()
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "2.0.0"
    }

# Authentication endpoints
@app.post("/auth/login")
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name
        }
    }

@app.post("/auth/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        role=user_data.role,
        full_name=user_data.full_name
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "message": "User created successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name
        }
    }

# Student results endpoints
@app.get("/results")
async def get_results(
    student_id: str = None,
    class_name: str = None,
    session: str = None,
    term: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(StudentResult)
    
    if student_id:
        query = query.filter(StudentResult.student_id == student_id)
    if class_name:
        query = query.filter(StudentResult.class_name == class_name)
    if session:
        query = query.filter(StudentResult.session == session)
    if term:
        query = query.filter(StudentResult.term == term)
    
    results = query.all()
    return results

@app.post("/results")
async def create_result(result_data: StudentResultCreate, db: Session = Depends(get_db)):
    result = StudentResult(**result_data.dict())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result

# Broadcast endpoints
@app.get("/broadcasts")
async def get_broadcasts(db: Session = Depends(get_db)):
    broadcasts = db.query(Broadcast).order_by(Broadcast.created_at.desc()).all()
    return broadcasts

@app.post("/broadcasts")
async def create_broadcast(broadcast_data: BroadcastCreate, db: Session = Depends(get_db)):
    broadcast = Broadcast(**broadcast_data.dict())
    db.add(broadcast)
    db.commit()
    db.refresh(broadcast)
    return broadcast

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
