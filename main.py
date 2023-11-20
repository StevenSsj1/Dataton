
from analisis import *
from fastapi import FastAPI, HTTPException, Query
from plots import *
from enum import Enum
from fastapi.responses import JSONResponse

app = FastAPI()


class TipoDelito(str, Enum):
    HOMICIDIO = "HOMICIDIO"
    SICARIATO = "SICARIATO"
    ASESINATO = "ASESINATO"


@app.get("/api/canton")
async def registros_por_canton(canton=Query(..., title="Canton")):
    datos = info_by_canton(canton)
    if datos != 'Error':
        return {"mensaje": f"Datos obtenidos correctamente del cantón {canton}", "datos": datos}
    raise HTTPException(status_code=404, detail="Canton no encontrado")


@app.get("/api/tasa_homicidios", response_class=JSONResponse,
         summary='tasa de delitos por cada 100.000 cuidadanos en las provincias')
def obtener_tasa_homicidios_provincia(delito: TipoDelito = Query(..., title="Tipo de Delito")):
    tipo_delito = delito.lower()
    datos_provincias = leer_tasa_homicidios_provincia(tipo_delito)
    return datos_provincias


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


@app.get("/api/distribucion-sexo-etnia")
async def generar_grafica_distribucion_sexo_etnia():
    datos_sexo, datos_etnia = distribucion_sexo_etnia()
    return {"mensaje": "Datos obtenidos correctamente para la distribución de sexo y etnia",
            "datos_sexo": datos_sexo.to_dict('records'),
            "datos_etnia": datos_etnia.to_dict('records')}


@app.get("/api/graficas/grafico-pastel-sexo-etnia")
async def generar_grafico_pastel_sexo_etnia():
    # Llama a la función del gráfico y devuelve la respuesta
    return grafico_pastel_sexo_etnia(*distribucion_sexo_etnia())


@app.get("/api/graficas/mapa-calor-homicidios-provincia")
async def generar_mapa_calor_homicidios_por_provincia():
    # Llama a la función del gráfico y devuelve la respuesta
    return mapa_calor_homicidios_por_provincia()