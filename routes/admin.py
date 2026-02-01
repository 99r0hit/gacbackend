from fastapi import APIRouter, Depends
from models import CreateUser, CreateBranch, CreateBatch
from db import supabase
from auth import authenticate, require_role

router = APIRouter()

@router.post("/create-user")
def create_user(data: CreateUser, email: str, password: str):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    supabase.table("users").insert({
        "name": data.name,
        "email": data.email,
        "password": data.password,
        "role": data.role,
        "active": True
    }).execute()

    return {"status": "user created"}


@router.post("/create-branch")
def create_branch(data: CreateBranch, email: str, password: str):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    supabase.table("branches").insert(data.dict()).execute()
    return {"status": "branch created"}


@router.post("/create-batch")
def create_batch(data: CreateBatch, email: str, password: str):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    supabase.table("batches").insert(data.dict()).execute()
    return {"status": "batch created"}

@router.get("/branches")
def get_branches(email: str, password: str):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    res = supabase.table("branches").select("*").execute()
    return res.data


@router.get("/coaches")
def get_coaches(email: str, password: str):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    res = supabase.table("users") \
        .select("id, name") \
        .eq("role", "coach") \
        .eq("active", True) \
        .execute()

    return res.data


@router.get("/batches")
def get_batches(email: str, password: str):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    res = supabase.table("batches") \
        .select("id, name, branch_id, coach_id") \
        .execute()

    return res.data
@router.get("/users")
def get_users(email: str, password: str):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    res = supabase.table("users") \
        .select("id, name, email, role, active") \
        .order("created_at", desc=True) \
        .execute()

    return res.data
