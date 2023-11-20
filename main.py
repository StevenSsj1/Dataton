from typing import Union
from analisis import *
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from plots import *
from enum import Enum
from fastapi.responses import StreamingResponse

app = FastAPI()


class TipoDelito(str, Enum):
    HOMICIDIO = "HOMICIDO"
    SICARIATO = "SICARIATO"
    ASESINATO = "ASESINATO"


@app.get("/api/canton")
async def registros_por_canton(canton=Query(..., title="Canton")):
    datos = info_by_canton(canton)
    if datos != 'Error':
        return {"mensaje": f"Datos obtenidos correctamente del cantón {canton}", "datos": datos}
    raise HTTPException(status_code=404, detail="Canton no encontrado")


# @app.get('/api/homicidios')
# async def tasa_homicidios_provincia():
#     try:
#         # Llama a la función que calcula las tasas de homicidios por provincia
#         resultado = tasa_homicidios_provincia()
#
#         # Convierte el DataFrame a un formato de cadena y devuelve la respuesta como texto plano
#         respuesta_texto = resultado.to_string(index=False)
#         return PlainTextResponse(content=respuesta_texto, media_type="text/plain")
#     except Exception as e:
#         # Manejo de errores
#         raise HTTPException(status_code=500, detail=f"Error al procesar la solicitud: {str(e)}")


@app.get('/api/homicidios/proporcion')
async def proporcion_delitos(delito: TipoDelito = Query(..., title="Tipo de Delito"),
                             arma=Query(..., title="Tipo de arma")):
    proporcion = arma_por_delito(delito, arma)
    return {'mensaje': f'Datos obtenidos correctamente del delito {delito} con {arma}',
            'datos': proporcion}


@app.get("/api/graficas")
async def generar_grafica_endpoint(delito: TipoDelito = Query(..., title="Tipo de Delito")):
    if not delito in TipoDelito:
        raise HTTPException(status_code=422, detail="Valor no encontrado en las opciones permitidas")
    return distribucion_por_edad(str(delito))
