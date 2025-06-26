from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["colegio_games"]

# Colección de usuarios
users_collection = db["usuarios"]

# Colección de juegos
juegos_collection = db["juegos"]