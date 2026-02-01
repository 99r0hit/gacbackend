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

@router.post("/assign-student")
def assign_student(
    payload: dict,
    email: str,
    password: str
):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    student_id = payload.get("student_id")
    batch_id = payload.get("batch_id")

    if not student_id or not batch_id:
        raise HTTPException(status_code=400, detail="student_id and batch_id required")

    # validate student
    student = supabase.table("users") \
        .select("id, role") \
        .eq("id", student_id) \
        .single() \
        .execute()

    if student.data["role"] != "student":
        raise HTTPException(status_code=400, detail="User is not a student")

    # check duplicate
    existing = supabase.table("student_batch") \
        .select("*") \
        .eq("student_id", student_id) \
        .eq("batch_id", batch_id) \
        .execute()

    if existing.data:
        raise HTTPException(status_code=400, detail="Already assigned")

    supabase.table("student_batch").insert({
        "student_id": student_id,
        "batch_id": batch_id
    }).execute()

    return {"status": "assigned"}

@router.get("/assignments")
def get_assignments(email: str, password: str):
    admin = authenticate(email, password)
    require_role(admin, "admin")

    res = supabase.table("student_batch").select(
        "student_id, batch_id"
    ).execute()

    return res.data


