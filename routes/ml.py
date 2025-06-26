from fastapi import APIRouter
from database import juegos_collection
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from joblib import dump

router = APIRouter()

@router.post("/entrenar-modelo")
async def entrenar_modelo():
    datos = await juegos_collection.find({"nivel": {"$exists": True}}).to_list(length=1000)
    if len(datos) < 10:
        return {"error": "Se requieren al menos 10 datos con nivel para entrenar"}

    df = pd.DataFrame(datos)
    X = df[["aciertos", "fallos", "tiempo"]]
    y = df["nivel"]

    modelo = DecisionTreeClassifier().fit(X, y)
    dump(modelo, "ml/modelo_actualizado.joblib")

    return {"message": "Modelo entrenado correctamente"}