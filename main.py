from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = FastAPI()

# CORS para permitir peticiones desde Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a MongoDB Atlas
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://cessenati:xpv604NPuoflyjaO@databasegus.aafystp.mongodb.net/?retryWrites=true&w=majority&appName=databasegus")
client = MongoClient(MONGO_URI)
db = client["colegio_games"]
users_collection = db["usuarios"]

# Modelos de datos
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

# Helper para convertir documentos BSON
def usuario_dict(doc):
    return {
        "id": str(doc.get("_id")),
        "parentName": doc.get("parentName"),
        "parentLastName": doc.get("parentLastName"),
        "parentEmail": doc.get("parentEmail"),
        "childName": doc.get("childName"),
        "childLastName": doc.get("childLastName"),
        "courses": doc.get("courses", []),
    }

# Rutas
@app.get("/users/health")
def health():
    return {"status": "ok"}

@app.post("/register", status_code=201)
def register_user(user: Usuario):
    if users_collection.find_one({"parentEmail": user.parentEmail}):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    result = users_collection.insert_one(user.dict())
    saved_user = users_collection.find_one({"_id": result.inserted_id})
    return usuario_dict(saved_user)

@app.post("/login")
def login_user(data: LoginInput):
    user = users_collection.find_one({"parentEmail": data.email})
    if not user or user.get("parentPassword") != data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return usuario_dict(user)

@app.get("/users/{email}")
def get_user_by_email(email: str):
    user = users_collection.find_one({"parentEmail": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_dict(user)

@app.put("/users/{email}")
def update_user(email: str, updated_data: dict):
    user = users_collection.find_one({"parentEmail": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Campos que se pueden actualizar (sin cambiar email ni contraseña)
    update_fields = {}
    for field in ["parentName", "parentLastName", "childName", "childLastName", "courses"]:
        if field in updated_data:
            update_fields[field] = updated_data[field]

    users_collection.update_one({"parentEmail": email}, {"$set": update_fields})
    updated_user = users_collection.find_one({"parentEmail": email})
    return usuario_dict(updated_user)
