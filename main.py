from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user  # importa tu router

app = FastAPI()

origins = [
    "http://localhost:51749",   # tu frontend local
    "http://localhost:5173",    # otro posible puerto
    "http://localhost:50991",    # otro posible puerto común de Flutter
    "https://app-abj-frontend.web.app",  # si luego usas hosting
    "https://app-abj-backend.onrender.com",  # opcional: para permitir fetch interno
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