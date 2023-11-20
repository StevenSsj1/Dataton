import matplotlib.pyplot as plt
import pandas as pd
from fastapi.responses import StreamingResponse
import io

reader = pd.read_csv('mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv',
                     delimiter=';', encoding='ISO-8859-1')
df = pd.DataFrame(reader)

def distribucion_por_edad(tipo_delito:str):
    delito = tipo_delito.split(".")
    df_edades_con_mas_homicidios = df[df['Tipo Muert.'] == delito[1]].groupby('Edad').size().reset_index(
        name='Numero de Homicidios')
    # Crea un gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(df_edades_con_mas_homicidios['Edad'], df_edades_con_mas_homicidios['Numero de Homicidios'])

    ax.set_xlabel(f'Edades de personas fallecidad por {delito[1]}')
    ax.set_ylabel(f'Número de personas fallecidas por {delito[1]}')
    ax.set_title(f'Edades')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.clf()
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")



# def distribucion_por_edad(edad_maxima):
#     # Crea un gráfico de barras
#     plt.bar(df['Provincia'], df['Edad con mas Homicidios'])
#     plt.xlabel('Provincia')
#     plt.ylabel('Edad con mas Homicidios')
#     plt.title('Edad con mas Homicidios en las Provincias')
#
#
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     plt.clf()
#     return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")

