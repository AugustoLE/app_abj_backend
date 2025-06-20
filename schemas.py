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