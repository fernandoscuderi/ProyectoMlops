#Importo librerias a utilizar
import pandas as pd
import numpy as np
import ast
from datetime import datetime
import calendar
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
from wordcloud import WordCloud, STOPWORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings("ignore")

# Leo los dataset con pandas
dfMovies = pd.read_csv('movies_dataset.csv')
dfCredits = pd.read_csv('credits.csv')

#Elimino las columnas que no se van a usar
dfMovies = dfMovies.drop(["video","imdb_id","adult","original_title","poster_path","homepage"],  axis=1)

##Convierto la columna fecha en formato AAA-MM-DD
dfMovies['release_date'] = pd.to_datetime(dfMovies['release_date'], errors='coerce')
dfMovies['release_date'] = dfMovies['release_date'].dt.strftime('%Y-%m-%d')

#Elimino los registros que contienen valores nulos en la columna "release_date"
dfMovies = dfMovies.dropna(subset=["release_date"])

#Convierto las columnas "id" al mismo tipo de dato (int) para poder hacer merge entre los dos dataFrames
dfCredits['id'] = dfCredits['id'].astype('Int64')
dfMovies['id'] = dfMovies['id'].astype('Int64')
df= pd.merge(dfMovies, dfCredits, on='id')

#Completo con Ceros los valores nulos de la columna "revenue"
df["revenue"] = df["revenue"].fillna(0)

#Extraigo el año de la columna "releae_date" y creo una nueva columna "release_year" con el mismo
df['release_date'] = pd.to_datetime(df['release_date'])
df["release_year"] = df["release_date"].dt.year

#Convierto en float la columna "budget"
df["budget"] = df["budget"].astype(float)

#Creo una funcion que devuelva 0 si falta algun valor, o si el denominador es = 0
def divide_columns(a, b):
    if pd.isnull(a) or pd.isnull(b) or b == 0:
        return 0
    else:
        return a / b

#Creo la columna que realiza la division entre "revenue" y "budget" usando la funcion anterior
df["return"] = df.apply(lambda row: divide_columns(row["revenue"], row["budget"]), axis=1)

#Creo una funcion que convierta el string contenido en la columna a tipo de dato diccionario y devuelva los valores de la clave "name"

def extrae_nombre(lista):
        if type(lista) != str:
            return None
        else:
            diccionario = ast.literal_eval(lista)
            nombre = diccionario["name"]
            return nombre
    
#Utilizo la funcion creada para hacer una nueva columna que contenga solo los nombres del diccionario
df["belongs_to_collection2"] = df["belongs_to_collection"].apply(extrae_nombre)



#Elimino la antigua columna, la renombro la nueva con el mismo nombre que la eliminada, y la ubico en su index orginal
df = df.drop("belongs_to_collection", axis=1)

df.rename(columns={"belongs_to_collection2": "belongs_to_collection"}, inplace=True)

columnas = df.columns.tolist()
df= df.reindex(columns=["belongs_to_collection"] + columnas[:-1])

#Creo la funcion que extrae los valores de la clave "name" de la lista de diccionarios
#(es necesario convertir el string que contiene la lista a tipo de dato list)
def extrae_nombre_de_listas(listaParam):
    if type(listaParam) != str:
        return None
    else:
        generosLista = ast.literal_eval(listaParam)
        nombres = []
        for i in generosLista:
                nombre = i["name"]
                nombres.append(nombre)
        return nombres
    
#Aplico la funcion en la columna "genres"
df["genres2"] = df["genres"].apply(extrae_nombre_de_listas)


#Elimino la antigua columna, la renombro con su respectivo nombre y en su index original
df = df.drop("genres", axis=1)

df.rename(columns={"genres2": "genres"}, inplace=True)

columnas = df.columns.tolist()
genres = columnas.pop(columnas.index('genres'))
columnas.insert(2, genres)
df = df.reindex(columns=columnas)

#Aplico la funcion creada anteriormente para extraer nombres de la columna "production_companies"
df["production_companies2"] = df["production_companies"].apply(extrae_nombre_de_listas)


#Elimino la antigua columna, la renombro con su respectivo nombre y en su index original
df = df.drop("production_companies", axis=1)

df.rename(columns={"production_companies2": "production_companies"}, inplace=True)

columnas = df.columns.tolist()
production_companies = columnas.pop(columnas.index('production_companies'))
columnas.insert(7, production_companies)
df = df.reindex(columns=columnas)

#Aplico la funcion creada anteriormente para extraer nombres de la columna "production_countries"
df["production_countries2"] = df["production_countries"].apply(extrae_nombre_de_listas)


#Elimino la antigua columna, la renombro con su respectivo nombre y en su index original
df = df.drop("production_countries", axis=1)

df.rename(columns={"production_countries2": "production_countries"}, inplace=True)

columnas = df.columns.tolist()
production_countries = columnas.pop(columnas.index('production_countries'))
columnas.insert(8, production_countries)
df = df.reindex(columns=columnas)

#Aplico la funcion creada anteriormente para extraer nombres de la columna "spoken_languages"
df["spoken_languages2"] = df["spoken_languages"].apply(extrae_nombre_de_listas)


#Elimino la antigua columna, la renombro con su respectivo nombre y en su index original
df = df.drop("spoken_languages", axis=1)

df.rename(columns={"spoken_languages2": "spoken_languages"}, inplace=True)

columnas = df.columns.tolist()
spoken_languages = columnas.pop(columnas.index('spoken_languages'))
columnas.insert(12, spoken_languages)
df = df.reindex(columns=columnas)

#Aplico la funcion creada anteriormente para extraer nombres de la columna "cast"
df["cast2"] = df["cast"].apply(extrae_nombre_de_listas)


#Elimino la antigua columna, la renombro con su respectivo nombre y en su index original
df = df.drop("cast", axis=1)

df.rename(columns={"cast2": "cast"}, inplace=True)

columnas = df.columns.tolist()
cast = columnas.pop(columnas.index('cast'))
columnas.insert(17, cast)
df = df.reindex(columns=columnas)

#Creo una funcion para extraer el director en la lista de la columna "crew"
def extrae_director(listaParam):
    if type(listaParam) != str:
        return None
    else:
        lista = ast.literal_eval(listaParam)
        nombres = []
        indice = 0
        for i, dicc in enumerate(lista):
                        if dicc["job"] == "Director":
                            indice = i
                            if indice >= 0:                        
                                nombres.append(lista[indice]["name"])
    return nombres

#Aplico la funcion creada anteriormente para extraer nombres de la columna "crew"
df["crew2"] = df["crew"].apply(extrae_director)

#Elimino la antigua columna, la renombro con su respectivo nombre y en su index original
df = df.drop("crew", axis=1)

df.rename(columns={"crew2": "crew"}, inplace=True)

columnas = df.columns.tolist()
crew = columnas.pop(columnas.index('crew'))
columnas.insert(18, crew)
df = df.reindex(columns=columnas)

