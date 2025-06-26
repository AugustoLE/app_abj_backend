from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import user, game, ml

app = FastAPI()

origins = [
    "https://app-abj-render.onrender.com",  # si luego usas hosting
    "https://app-abj-backend.onrender.com",  # opcional: para permitir fetch interno
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(user.router)
app.include_router(game.router)
app.include_router(ml.router)

@app.get("/")
async def root():
    return {"message": "Servidor backend con ML funcionando"}