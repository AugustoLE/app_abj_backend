from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from typing import List

from models import Usuario, LoginInput
from database import users_collection
from schemas import usuario_dict

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Backend funcionando con motor"}

@router.get("/users/health")
async def health():
    return {"status": "ok"}

@router.post("/register", status_code=201)
async def register_user(user: Usuario):
    existing = await users_collection.find_one({"parentEmail": user.parentEmail})
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    result = await users_collection.insert_one(user.dict())
    saved_user = await users_collection.find_one({"_id": result.inserted_id})
    return usuario_dict(saved_user)

@router.post("/login")
async def login_user(data: LoginInput):
    user = await users_collection.find_one({"parentEmail": data.email})
    if not user or user.get("parentPassword") != data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return usuario_dict(user)

@router.get("/users/{email}")
async def get_user_by_email(email: str):
    user = await users_collection.find_one({"parentEmail": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_dict(user)

@router.put("/users/{email}")
async def update_user(email: str, updated_data: dict):
    user = await users_collection.find_one({"parentEmail": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    fields = ["parentName", "parentLastName", "childName", "childLastName", "courses"]
    update_fields = {field: updated_data[field] for field in fields if field in updated_data}
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos válidos para actualizar")

    await users_collection.update_one({"parentEmail": email}, {"$set": update_fields})
    updated_user = await users_collection.find_one({"parentEmail": email})
    return usuario_dict(updated_user)