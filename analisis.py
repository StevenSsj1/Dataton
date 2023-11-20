import math

import pandas as pd

# Lectura del archivo .csv
poblacion_provincia = [881394, 209933, 281396, 186869, 524004, 488716
    , 715751, 643654, 33042, 4387434, 476257]

reader = pd.read_csv('mdi_homicidiosintencionales_pm_2023_enero_septiembre.csv',
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


# def tasa_homicidios_provincia():
#     # Agrupa por provincia y cuenta el número de homicidios en cada provincia
#     homicidios_por_provincia = df[df['Tipo Muert.'] == 'HOMICIDIO'].groupby('Provincia').size().reset_index(
#         name='Numero de Homicidios')
#     datos_provincias = combinar_listas_en_dataframe(lista_provincias, poblacion_provincias)
#     datos_combinados = pd.merge(homicidios_por_provincia, datos_provincias, on='Provincia')
#     datos_combinados['Resultado'] = (datos_combinados['Numero de Homicidios'] / datos_combinados['Poblacion'] * 100000)
#     return datos_combinados[['Provincia', 'Resultado']]

def arma_por_delito(tipo_delito: str, tipo_arma: str):
    delito = tipo_delito.split(".")
    homicidios_intencionales = df[df['Tipo Muert.'] == delito[0]]
    proporcion_con_arma_de_fuego = ((homicidios_intencionales['Arma'] == tipo_arma).mean())*100
    resultado = math.floor(proporcion_con_arma_de_fuego)
    return resultado


arma_por_delito('ASESINATO', 'ARMA DE FUEGO')
