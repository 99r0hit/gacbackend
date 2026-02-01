from fastapi import HTTPException
from db import supabase

def authenticate(email: str, password: str):
    res = supabase.table("users") \
        .select("*") \
        .eq("email", email) \
        .eq("password", password) \
        .eq("active", True) \
        .execute()

    if not res.data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return res.data[0]


def require_role(user, role: str):
    if user["role"] != role:
        raise HTTPException(status_code=403, detail="Forbidden")
