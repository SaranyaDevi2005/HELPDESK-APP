from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import UserRegister, UserLogin
from database import users_col
import bcrypt
import jwt
import os
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET", "helpdesk-secret-key-change-in-prod")
JWT_EXPIRY_HOURS = 24

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_token(user_data: dict) -> str:
    payload = {
        "sub": user_data["username"],
        "user_type": user_data["user_type"],
        "role": user_data["role"],
        "department": user_data.get("department"),
        "employee_id": user_data.get("employee_id"),
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

@app.post("/register")
def register(user: UserRegister):
    if users_col.find_one({"username": user.username}):
        raise HTTPException(400, "Username already exists")
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_col.insert_one({
        "username": user.username,
        "password": hashed,
        "email": user.email,
        "user_type": user.user_type,
        "department": user.department,
        "role": user.role,
        "employee_id": user.employee_id
    })
    return {"message": "Registered successfully"}

@app.post("/login")
def login(user: UserLogin):
    db_user = users_col.find_one({"username": user.username})
    if not db_user or not bcrypt.checkpw(user.password.encode(), db_user["password"]):
        raise HTTPException(401, "Invalid credentials")
    token = create_token(db_user)
    return {
        "token": token,
        "username": db_user["username"],
        "user_type": db_user["user_type"],
        "role": db_user["role"],
        "department": db_user.get("department"),
        "employee_id": db_user.get("employee_id")
    }

@app.get("/verify")
def verify(current_user: dict = Depends(verify_token)):
    return {"valid": True, "user": current_user["sub"]}

@app.get("/health")
def health():
    return {"status": "ok"}
