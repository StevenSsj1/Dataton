from typing import Union

import pandas as pd
from pandas import DataFrame

# Lee el archivo CSV
reader = pd.read_csv('Ejemplo.csv', delimiter=';', encoding='ISO-8859-1')
df = pd.DataFrame(reader).dropna()


#def get_dats_by_head(Headers: str) -> Union[DataFrame]:
 #   return df.filter(items=[f'{Headers}']) if Headers in df.keys() else pd.DataFrame()
def get_dats_by_head(Headers: Union[str, list[str]]) -> Union[DataFrame]:
    Headers = [Headers]
    return df[Headers] if all(header in df.columns for header in Headers) else pd.DataFrame()


print(get_dats_by_head('Fechas'))
