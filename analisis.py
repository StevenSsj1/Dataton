import math

import pandas as pd
import json
# Lectura del archivo .csv
poblacion_provincia = [881394, 209933, 281396, 186869, 524004, 488716
    ,715751, 643654, 33042, 4387434, 476257, 521154, 921763, 1562079,
    196535, 133705, 161338, 114202, 3228233, 401178, 458580, 230503,
    590600, 120416, 41907]

reader = pd.read_csv('datasets/mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv',
                     delimiter=';', encoding='ISO-8859-1')
df = pd.DataFrame(reader)
row, column = df.shape  # numeros de filas y columnas en el csv


# info = df.info() # informacion sobre el tipo de dato de la columna y sabes si tiene valores nulos

def info_by_canton(canton: str) -> dict:
    if canton not in df['Cantón'].unique():
        return 'Error'
    datos_canton = df[df['Cantón'] == canton][['Tipo Muert.',
                                               'Probable Causa M.',
                                               'Arma']].to_dict('records')
    return datos_canton


def obtener_lista_provincias_con_homicidios(df):
    # Filtra el DataFrame para incluir solo las filas con 'Tipo Muert.' igual a 'HOMICIDIO'
    df_homicidios = df[df['Tipo Muert.'] == 'HOMICIDIO']
    # Utiliza el método unique() para obtener las provincias con homicidios sin repetir
    lista_provincias_con_homicidios = df_homicidios['Provincia'].unique().tolist()
    ordenados = sorted(lista_provincias_con_homicidios)

    return ordenados


def combinar_listas_en_dataframe(lista_provincias, lista_poblacion):
    # Crear un DataFrame con las listas de provincias y población
    datos = pd.DataFrame({'Provincia': lista_provincias, 'Poblacion': lista_poblacion})

    return datos


lista_provincias = obtener_lista_provincias_con_homicidios(df)
poblacion_provincias = poblacion_provincia * (23 // len(poblacion_provincia)) + poblacion_provincia[
                                                                                :23 % len(poblacion_provincia)]


def tasa_homicidios_provincia():
    # Agrupa por provincia y cuenta el número de homicidios en cada provincia
    homicidios_por_provincia = df[df['Tipo Muert.'] == 'SICARIATO'].groupby('Provincia').size().reset_index(
        name='Numero de Homicidios')
    datos_provincias = combinar_listas_en_dataframe(lista_provincias, poblacion_provincias)
    datos_combinados = pd.merge(homicidios_por_provincia, datos_provincias, on='Provincia')
    datos_combinados['Resultado'] = (datos_combinados['Numero de Homicidios'] / datos_combinados['Poblacion'] * 100000)
    return print(datos_combinados[['Provincia', 'Resultado']])

def leer_tasa_homicidios_provincia(delito:str):
    with open(f"tasa_{delito}_provincia.json", "r") as file:
        datos_provincias = json.load(file)
    return datos_provincias

def arma_por_delito_json(tipo_delito: str, tipo_arma: str):
    homicidios_intencionales = df[df['Tipo Muert.'] == tipo_delito]
    proporcion_con_arma_de_fuego = ((homicidios_intencionales['Arma'] == tipo_arma).mean())*100
    resultado = math.floor(proporcion_con_arma_de_fuego)
    return resultado
def arma_por_delito():
    with open("arma_por_delito.json", "r") as file:
        datos = json.load(file)
    return datos


def distribucion_temporal():
    # Realiza la lectura del archivo CSV y ajusta el formato de fecha directamente
    df = pd.read_csv('datasets/mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv', delimiter=';', encoding='ISO-8859-1', parse_dates=['Fecha Infracción'], dayfirst=True)
    # Transforma la columna 'Fecha Infracción' a formato de fecha
    df['Fecha Infracción'] = pd.to_datetime(df['Fecha Infracción'])

    # Crea una nueva columna para el mes
    df['Mes'] = df['Fecha Infracción'].dt.month

    # Agrupa por mes y cuenta el número de homicidios
    distribucion_temporal = df.groupby('Mes').size().reset_index(name='Numero de Homicidios por Mes')

    return distribucion_temporal

def distribucion_sexo_etnia():
    # Agrupa por sexo y cuenta el número de homicidios
    distribucion_sexo = df.groupby('Sexo').size().reset_index(name='Numero de Homicidios por Sexo')

    # Agrupa por etnia y cuenta el número de homicidios
    distribucion_etnia = df.groupby('Etnia').size().reset_index(name='Numero de Homicidios por Etnia')

    return distribucion_sexo, distribucion_etnia


