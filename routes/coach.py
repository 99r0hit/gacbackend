from fastapi import APIRouter
from models import AttendanceRecord, SessionRecord
from db import supabase
from auth import authenticate, require_role

router = APIRouter()

@router.post("/attendance")
def mark_attendance(data: AttendanceRecord, email: str, password: str):
    coach = authenticate(email, password)
    require_role(coach, "coach")

    supabase.table("attendance").insert(data.dict()).execute()
    return {"status": "attendance saved"}


@router.post("/session")
def add_session(data: SessionRecord, email: str, password: str):
    coach = authenticate(email, password)
    require_role(coach, "coach")

    supabase.table("sessions").insert(data.dict()).execute()
    return {"status": "session saved"}
