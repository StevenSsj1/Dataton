from typing import Union
from analisis import *
from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
app = FastAPI()


@app.get("api/{canton}")
def read_root(canton: str):
    datos = info_by_canton(canton)
    if datos != 'Error':
        return {"mensaje": f"Datos obtenidos correctamente del cantón {canton}", "datos": datos}
    raise HTTPException(status_code=404, detail="Canton no encontrado")


@app.get('/api/homicidios')
async def tasa_homicidios_provincia_endpoint():
    try:
        # Llama a la función que calcula las tasas de homicidios por provincia
        resultado = tasa_homicidios_provincia()

        # Convierte el DataFrame a un formato de cadena y devuelve la respuesta como texto plano
        respuesta_texto = resultado.to_string(index=False)
        return PlainTextResponse(content=respuesta_texto, media_type="text/plain")
    except Exception as e:
        # Manejo de errores
        raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")
