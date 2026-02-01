from fastapi import APIRouter, HTTPException
from models import AttendanceRecord, SessionRecord
from db import supabase
from auth import authenticate, require_role

router = APIRouter(prefix="/coach", tags=["Coach"])

@router.post("/attendance")
def mark_attendance(payload: dict, email: str, password: str):
    coach = authenticate(email, password)
    require_role(coach, "coach")

    records = []
    for item in payload["attendance"]:
        records.append({
            "student_id": item["student_id"],
            "batch_id": payload["batch_id"],
            "date": payload["date"],
            "present": item["present"]
        })

    supabase.table("attendance").insert(records).execute()
    return {"status": "attendance saved"}


@router.post("/session")
def create_session(payload: dict, email: str, password: str):
    coach = authenticate(email, password)
    require_role(coach, "coach")

    supabase.table("sessions").insert({
        "date": payload["date"],
        "time": payload["time"],
        "batch_id": payload["batch_id"],
        "topic": payload.get("topic"),
        "notes": payload.get("notes")
    }).execute()

    return {"status": "session created"}



@router.get("/branches")
def get_coach_branches(email: str, password: str):
    coach = authenticate(email, password)
    require_role(coach, "coach")

    batches = supabase.table("batches") \
        .select("branch_id") \
        .eq("coach_id", coach["id"]) \
        .execute()

    branch_ids = list({b["branch_id"] for b in batches.data})

    if not branch_ids:
        return []

    res = supabase.table("branches") \
        .select("*") \
        .in_("id", branch_ids) \
        .execute()

    return res.data
@router.get("/students")
def get_students(branch_id: str, email: str, password: str):
    coach = authenticate(email, password)
    require_role(coach, "coach")

    batches = supabase.table("batches") \
        .select("id") \
        .eq("coach_id", coach["id"]) \
        .eq("branch_id", branch_id) \
        .execute()

    batch_ids = [b["id"] for b in batches.data]

    if not batch_ids:
        return []

    sb = supabase.table("student_batch") \
        .select("student_id") \
        .in_("batch_id", batch_ids) \
        .execute()

    student_ids = [s["student_id"] for s in sb.data]

    if not student_ids:
        return []

    students = supabase.table("users") \
        .select("id, name") \
        .in_("id", student_ids) \
        .execute()

    return students.data



