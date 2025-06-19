from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Crear instancia FastAPI
app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplazar con dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexión a MongoDB Atlas usando .env
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("Falta definir MONGO_URI en el archivo .env")

client = AsyncIOMotorClient(MONGO_URI)
db = client["colegio_games"]
users_collection = db["usuarios"]

# Modelos
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

# Convertidor BSON a dict JSON serializable
def usuario_dict(doc):
    return {
        "id": str(doc["_id"]),
        "parentName": doc["parentName"],
        "parentLastName": doc["parentLastName"],
        "parentEmail": doc["parentEmail"],
        "childName": doc["childName"],
        "childLastName": doc["childLastName"],
        "courses": doc["courses"],
    }

# Rutas
@app.get("/")
async def root():
    return {"message": "Backend funcionando con motor"}

@app.get("/users/health")
async def health():
    return {"status": "ok"}

@app.post("/register", status_code=201)
async def register_user(user: Usuario):
    existing = await users_collection.find_one({"parentEmail": user.parentEmail})
    if existing:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    result = await users_collection.insert_one(user.dict())
    saved_user = await users_collection.find_one({"_id": result.inserted_id})
    return usuario_dict(saved_user)

@app.post("/login")
async def login_user(data: LoginInput):
    user = await users_collection.find_one({"parentEmail": data.email})
    if not user or user.get("parentPassword") != data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return usuario_dict(user)

@app.get("/users/{email}")
async def get_user_by_email(email: str):
    user = await users_collection.find_one({"parentEmail": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario_dict(user)

@app.put("/users/{email}")
async def update_user(email: str, updated_data: dict):
    user = await users_collection.find_one({"parentEmail": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    fields = ["parentName", "parentLastName", "childName", "childLastName", "courses"]
    update_fields = {field: updated_data[field] for field in fields if field in updated_data}
    await users_collection.update_one({"parentEmail": email}, {"$set": update_fields})
    updated_user = await users_collection.find_one({"parentEmail": email})
    return usuario_dict(updated_user)