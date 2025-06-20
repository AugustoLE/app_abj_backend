from pydantic import BaseModel, EmailStr
from typing import List

class Usuario(BaseModel):
    parentName: str
    parentLastName: str
    parentEmail: EmailStr
    parentPassword: str
    childName: str
    childLastName: str
    courses: List[str]

class LoginInput(BaseModel):
    email: EmailStr
    password: str