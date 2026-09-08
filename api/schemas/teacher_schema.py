from pydantic import BaseModel
from api.schemas.admin_schemas import ClassInfo


class TeacherResponse(BaseModel):
    teacher_id : int
    full_name : str
    email : str
    phone_number : str
    classes: list[ClassInfo] = []


class TeacherCreate(BaseModel):
    full_name : str
    email : str
    password : str
    phone_number : str

class TeacherUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone_number: str | None = None
