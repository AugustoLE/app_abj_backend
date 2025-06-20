from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user  # importa tu router

app = FastAPI()

origins = [
    "http://localhost:50991",
    "https://app-abj-backend.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(user.router)