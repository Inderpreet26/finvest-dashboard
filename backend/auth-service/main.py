from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Auth Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake users database
users_db = {}

class RegisterUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"service": "Auth Service", "status": "running"}

@app.post("/register")
def register(user: RegisterUser):
    if user.email in users_db:
        return {"success": False, "message": "User already exists"}
    users_db[user.email] = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    return {"success": True, "message": "User registered successfully"}

@app.post("/login")
def login(user: LoginUser):
    if user.email not in users_db:
        return {"success": False, "message": "User not found"}
    if users_db[user.email]["password"] != user.password:
        return {"success": False, "message": "Wrong password"}