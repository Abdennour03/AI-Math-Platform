from pydantic import BaseModel


class StudentResponse(BaseModel):
    student_id :int
    full_name : str
    email : str
    phone_number : str
    level :str
    class_id: int | None = None

class StudentCreate(BaseModel):
    full_name : str
    email : str
    password :str
    phone_number : str
    level :str
    class_id: int | None = None

class StudentUpdate(BaseModel):
    full_name: str | None = None
    email: str | None = None
    password: str | None = None
    phone_number: str | None = None
    level: str | None = None    
    class_id: int | None = None