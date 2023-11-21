import matplotlib.pyplot as plt
import pandas as pd
from fastapi.responses import StreamingResponse
import io
import seaborn as sns

reader = pd.read_csv('datasets/mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv',
                     delimiter=';', encoding='ISO-8859-1')
df = pd.DataFrame(reader)

def distribucion_por_edad(tipo_delito:str):
    delito = tipo_delito.split(".")
    df_edades_con_mas_homicidios = df[df['Tipo Muert.'] == delito[1]].groupby('Edad').size().reset_index(
        name='Numero de Homicidios')
    # Crea un gráfico de barras
    fig, ax = plt.subplots()
    ax.bar(df_edades_con_mas_homicidios['Edad'], df_edades_con_mas_homicidios['Numero de Homicidios'])

    ax.set_xlabel(f'Edades de personas fallecidas por {delito[1]}')
    ax.set_ylabel(f'Número de personas fallecidas por {delito[1]}')
    ax.set_title(f'Edades')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.clf()
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")


def grafico_pastel_sexo_etnia(distribucion_sexo, distribucion_etnia):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.pie(distribucion_sexo['Numero de Homicidios por Sexo'], labels=distribucion_sexo['Sexo'], autopct='%1.1f%%')
    ax1.set_title('Distribución de Homicidios por Sexo')

    ax2.pie(distribucion_etnia['Numero de Homicidios por Etnia'], labels=distribucion_etnia['Etnia'], autopct='%1.1f%%')
    ax2.set_title('Distribución de Homicidios por Etnia')

    # Devuelve los datos de los gráficos
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.clf()
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")


def mapa_calor_homicidios_por_provincia():
    # Realiza la lectura del archivo CSV y ajusta el formato de fecha directamente
    df = pd.read_csv('datasets/mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv', delimiter=';', encoding='ISO-8859-1',
                     parse_dates=['Fecha Infracción'], dayfirst=True)

    # Agregar una nueva columna 'Mes' extrayendo el mes de 'Fecha Infracción'
    df['Mes'] = df['Fecha Infracción'].dt.month_name()

    homicidios_por_provincia = df.groupby(['Provincia', 'Mes']).size().reset_index(name='Numero de Homicidios')
    pivot_table = homicidios_por_provincia.pivot_table(index='Provincia', columns='Mes', values='Numero de Homicidios',
                                                       fill_value=0)
    sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='g', linewidths=.5)
    plt.title('Mapa de Calor de Homicidios por Provincia y Mes')

    # Devuelve los datos del gráfico
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.clf()
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")


