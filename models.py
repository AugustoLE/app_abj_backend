from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

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

class JuegoInput(BaseModel):
    nombre_juego: str
    aciertos: int
    fallos: int
    tiempo: Optional[float] = None
    nivel: Optional[str] = None
    fecha: Optional[datetime] = None