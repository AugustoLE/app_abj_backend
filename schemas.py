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

def juego_dict(doc):
    return {
        "id": str(doc.get("_id")),
        "parentEmail": doc.get("parentEmail"),
        "nombre_juego": doc.get("nombre_juego"),
        "aciertos": doc.get("aciertos"),
        "fallos": doc.get("fallos"),
        "tiempo": doc.get("tiempo"),
        "nivel": doc.get("nivel"),
        "fecha": doc.get("fecha")
    }