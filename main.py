from fastapi import FastAPI
import pandas as pd
import numpy as np
import ast
from datetime import datetime
import calendar

app = FastAPI()

df = pd.read_csv('archivo.csv')

#http://127.0.0.1:8000
df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d')

#Creo la funcion que devuelva la cantidad de peliculas estrenadas en el mes especificado por parametro, devuelve error de un mal ingreso de parametro y acepta mayusculas o minusculas.
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes):
    dicc_meses = {"enero": 1, "febrero":2, "marzo":3, "abril":4, "mayo":5, "junio":6, "julio":7, "agosto":8, "septiembre":9, "octubre":10, "noviembre":11, "diciembre":12}
    
    if mes in dicc_meses:
        for clave, valor in dicc_meses.items():
            if clave == mes.lower():
                numero_mes = valor

        cantidad = 0

        fechas_estreno = df["release_date"]
        for fecha in fechas_estreno:
         if fecha.month == int(numero_mes):
            cantidad += 1

        return str(cantidad) + " películas fueron estrenadas en los meses de " + str(mes).lower()
    else: return "El mes indicado no fue escrito correctamente"


    #Creo la funcion que devuelva la cantidad de peliculas estrenadas en el dia especificado por parametro, devuelve error de un mal ingreso de parametro y acepta mayuscula o minuscula.
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia):
    dicc_dias = {"lunes": "mon", "martes":"tue", "miercoles":"wed", "jueves":"thu", "viernes":"fri", "sabado":"sat", "domingo":"sun"}
    
    if dia.lower() in dicc_dias:
        for clave, valor in dicc_dias.items():
            if clave == dia.lower():
                dia_estreno = valor
    
                cantidad = 0
                fechas_estreno = df["release_date"]
    
                for fecha in fechas_estreno:
                    if fecha.strftime("%a").lower() == dia_estreno:
                        cantidad += 1

                return str(cantidad) + " películas fueron estrenadas en los dias " + str(dia).lower()
    else: return "El dia indicado no fue escrito correctamente"


    #Creo funcion que devuelve la pelicula buscada, su año de estreno y el score asignado por TheMoviesDataBase. Devuelve error si no la encuentra y acepta mayusculas o minusculas.
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo):

    titulos = df["title"]
    titulo_encontrado = 0

    for i, e in enumerate(titulos):
            if e.lower() == titulo.lower():
                titulo_encontrado = e
                indice = i

    if titulo_encontrado != 0:
        return "La pelicula " + titulo_encontrado + " fue estrenada en el año " + str(df["release_year"][indice]) +  " con una puntaje de " + str(df["popularity"][indice]) + " asignado por TheMoviesDataBase"
    else: return "La pelicula ingresada no fue encontrada" 


    #Creo funcion que devuelve la pelicula buscada con su año de estreno, cantidad de votos y promedio de puntajes. Devuelve error si no la encuentra y acepta mayusculas o minusculas.
@app.get("/votos_titulo/{titulo_film}")
def votos_titulo(titulo_film):
    titulos = df["title"]
    titulo_encontrado = None

    for i, e in enumerate(titulos):
            if e.lower() == titulo_film.lower() and df["vote_count"][i] >= 2000:
                titulo_encontrado = e
                indice = i
            elif e.lower() == titulo_film.lower() and df["vote_count"][i] < 2000:
                return "La pelicula no cuenta con la cantidad suficiente de votos"
            
    if titulo_encontrado:
        return "La pelicula " + titulo_encontrado + " fue estrenada en el año " + str(df["release_year"][indice]) +  " y cuenta con un total de " + str(df["vote_count"][indice]) + " valoraciones, y su puntaje promedio de reseñas es de " + str(df["vote_average"][indice])
    else: return "La pelicula ingresada no fue encontrada"


    #Creo la funcion que devuelve el actor y sus participaciones en films, con sus respectivos retornos. Devuelve error si no encuentra y acepta nombres con o sin mayusculas.
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor):

    cantidad_films = 0
    cantidad_retorno = 0
    
    actores = df["cast"]
    for i, lista in enumerate(actores):

        nombreEntero = nombre_actor.split()
        nombreEnteroMayus = [palabra.capitalize() for palabra in nombreEntero]
        nombreMayus = ' '.join(nombreEnteroMayus)

        if nombreMayus in lista:
            cantidad_films += 1
            cantidad_retorno += df["return"][i]
        
    if cantidad_films != 0:
        return f"El actor {nombreMayus} ha participado de {cantidad_films} films y ha conseguido un retorno de {round(cantidad_retorno,2)}, con un promedio de {round(cantidad_retorno/cantidad_films,2)} por filmacion "
    else: return "El actor no fue encontrado"


    #Creo la funcion que recibe el nombre del director por parametro y devuelve un dataframe con informacion sobre las peliculas. Devuelve error si no encuentra el director y acepta mayusculas o minusculas.
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director):

    peliculas = []
    fecha = []
    retorno_individual = []
    costo = []
    ganancia =[]
    cantidad_retorno = 0

    directores = df["crew"]

    nombreEntero = nombre_director.split()
    nombreEnteroMayus = [palabra.capitalize() for palabra in nombreEntero]
    nombreMayus = ' '.join(nombreEnteroMayus)

    for i, lista in enumerate(directores):

        if nombreMayus in lista:
            cantidad_retorno += df["return"][i]
            peliculas.append(df["title"][i])
            fecha.append(df["release_date"][i].date())
            retorno_individual.append(df["return"][i])
            costo.append(df["budget"][i])
            ganancia.append(df["revenue"][i])

    dfDirector = pd.DataFrame({'Peliculas': peliculas, 'Fecha': fecha, 'Retorno Individual': retorno_individual, "Costo" : costo, "Ganancia": ganancia})
 
    if peliculas:
        return dfDirector
    else: return "El director no fue encontrado"
    