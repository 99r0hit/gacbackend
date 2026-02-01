from pydantic import BaseModel
from typing import Optional
from datetime import date

class LoginRequest(BaseModel):
    email: str
    password: str


class CreateUser(BaseModel):
    name: str
    email: str
    password: str
    role: str


class CreateBranch(BaseModel):
    name: str
    location: Optional[str]


class CreateBatch(BaseModel):
    name: str
    branch_id: str
    coach_id: str


class AttendanceRecord(BaseModel):
    date: date
    batch_id: str
    student_id: str
    present: bool


class SessionRecord(BaseModel):
    date: date
    batch_id: str
    topic: str
    notes: Optional[str]
