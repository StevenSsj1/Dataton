from typing import Union
from lecturaDatos import get_dats_by_head
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/{headers}")
def read_root(headers: str):
    datos = get_dats_by_head(headers)
    if not datos.empty:
        return {"mensaje": "Datos obtenidos correctamente", "datos": datos.to_dict(orient='records')}
    raise HTTPException(status_code=404, detail="Persona no encontrada")


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
