from fastapi import APIRouter
from models import LoginRequest
from auth import authenticate

router = APIRouter()

@router.post("/login")
def login(data: LoginRequest):
    user = authenticate(data.email, data.password)
    return {
        "user_id": user["id"],
        "role": user["role"],
        "name": user["name"]
    }
