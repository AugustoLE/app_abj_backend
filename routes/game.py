from fastapi import APIRouter, HTTPException
from models import JuegoInput
from database import juegos_collection
from schemas import juego_dict
from datetime import datetime
import joblib
import os
import numpy as np

router = APIRouter()

@router.post("/juegos/{email}")
async def registrar_juego(email: str, juego: JuegoInput):
    data = juego.dict()
    data["parentEmail"] = email
    data["fecha"] = data.get("fecha") or datetime.utcnow()
    result = await juegos_collection.insert_one(data)
    return {"message": "Juego registrado", "id": str(result.inserted_id)}

@router.get("/juegos/{email}")
async def obtener_juegos(email: str):
    juegos = await juegos_collection.find({"parentEmail": email}).to_list(length=100)
    return [juego_dict(j) for j in juegos]

@router.get("/analisis/{email}")
async def analizar_jugador(email: str):
    juegos = await juegos_collection.find({"parentEmail": email}).to_list(length=100)
    if not juegos:
        raise HTTPException(status_code=404, detail="No se encontraron juegos")

    modelo_path = "ml/modelo_actualizado.joblib"
    if not os.path.exists(modelo_path):
        return {"message": "Modelo no entrenado aún"}

    modelo = joblib.load(modelo_path)
    descripciones = []

    for j in juegos:
        x = np.array([[j["aciertos"], j["fallos"], j.get("tiempo", 0)]])
        pred = modelo.predict(x)[0]
        descripciones.append({
            "juego": j["nombre_juego"],
            "nivel_estimado": pred,
            "aciertos": j["aciertos"],
            "fallos": j["fallos"]
        })

    return {
        "email": email,
        "resumen": descripciones,
        "mensaje": "Análisis basado en ML terminado"
    }