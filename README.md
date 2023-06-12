# **Machine Learning Operations (MLOps)**
---

## Links del proyecto
### *Acceso al repositorio GitHub : https://github.com/fernandoscuderi/ProyectoMlops*
### *Acceso al proyecto en Render : https://pi-ml-ops-fi7e.onrender.com/docs*
### *Acceso al video de demostración :https://drive.google.com/file/d/1fZZ2ypMqjBfGlHqZTdd5AOyhMlvs9rok/view?usp=sharing*
---

## **Objetivo del proyecto: <br>**
Dados dos DataSet (credits.csv y movies_dataset.csv) que proveen registros de estrenos de peliculas, se pide una crear una API con 6 funciones que devuelvan determinadas respuestas y un sistema de recomendación.
El proyecto fue abordado en tres etapas, ETL, EDA, y API (con las funciones). <br>
A continuación se describe en detalle los procesos de cada etapa.

## ETL (Ver archivo etl.py) <br>
- Como primer paso se realiza la unión de los dos DataSets, tomando el ID como referencia.

- Las columnas belongs_to_collection, production_companies, genres, spoken_languages , production_country, cres y cast están anidados, por lo que se lleva a cabo un proceso de limpieza de estas columnas para extraer únicamente los datos más relevantes.

- Los valores nulos de los campos revenue, budget fueron rellenados por el número 0.

- Los valores nulos del campo release fueron eliminados.

- Las fechas se llevan al formato AAAA-mm-dd, además se crea la columna release_year donde se extrae el año de la fecha de estreno.

- Se crea la columna con el retorno de inversión, llamada return, con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, se toma el valor 0.

- Se eliminan las columnas que no serán utilizadas, video, imdb_id, adult, original_title, poster_path y homepage.

- Una vez realizada la limpieza, se exporta un nuevo csv (df_limpio.csv) para trabajar con el posteriormente.

## EDA (Ver archivo eda.ipynb) <br>
- Inicialmente se realiza un analisis general del DataSet, utilizando .head para ver el formato y el contenido de las filas y columnas, .shape para visualizar la cantidad de las mismas, .info para ver en una lista los valores nulos y el tipo de datos que esta contiene.
También con la libreria missingno visualizamos en un grafico de barras las proporciones de valores nulos en el DataSet.

- Luego del analisis básico, exploramos algunas relaciones e información que nos brinda el archivo df_limpio, por ejemplo: <br>
Gráficos mostrando la cantidad de filmaciones producidas en determinado mes y en determinado día.

- Visualizo en un dataframe el director con mayor cantidad de peliculas y su retorno total.

- Visualizo en un dataframe los actores con mayor cantidad de peiculas y el promedio de votos.

- Visualizo las peliculas con mayor promedio de votos, con genero y actores.

- Visualizo los 10 paises con mayores producciones.

- Y para tener en cuenta a la hora de realizar el modelo de recomendación, analizo con una nube de palabras la columna "Title" y "Overviews.

## API, FUNCIONES, SISTEMA DE RECOMENDACIÓN (Ver archivo main.py) <br>
- Se importa el frameWork fastAPI y se lo utiliza para poder consumir los endpoints con las funciones correspondientes, estas son:

- def cantidad_filmaciones_mes( Mes ): Se ingresa un mes en idioma Español. Dvuelve la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
                    Retorno: X cantidad de películas fueron estrenadas en el mes de X.

- def cantidad_filmaciones_dia( Dia ): Se ingresa un día en idioma Español. Devuelve la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
                    Retorno: X cantidad de películas fueron estrenadas en los días X.

- def score_titulo( titulo_de_la_filmación ): Se ingresa el título de una filmación y devuelve como respuesta el título, el año de estreno y el score.
                    Retorno: La película X fue estrenada en el año X con un score/popularidad de X.

- def votos_titulo( titulo_de_la_filmación ): Se ingresa el título de una filmación y devuelve como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable debe contar con al menos 2000 valoraciones, caso contrario, devuelve un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
                    Retorno: La película X fue estrenada en el año X. La misma cuenta con un total de X valoraciones, con un promedio de X.

- def get_actor( nombre_actor ): Se ingresa el nombre de un actor que se encuentre dentro de un dataset y devuelve el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno. 
                    Retorno: El actor X ha participado de X cantidad de filmaciones, el mismo ha conseguido un retorno de X con un promedio de X por filmación

- def get_director( nombre_director ): Se ingresa el nombre de un director que se encuentre dentro de un dataset y devuelve el éxito del mismo medido a través del retorno. Además, devuelve el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

- Sistema de recomendación:

Se entrena nuestro modelo de machine learning para armar un sistema de recomendación de películas. Éste consiste en recomendar películas a los usuarios basándose en películas similares, la función las encuentra a partir de un título de referencia, utilizando técnicas de procesamiento de texto (TFidF) y cálculo de similitud de coseno. Proporciona una lista de las películas más similares y recomendadas para el usuario, devuelve 5 valores, cada uno siendo el string del nombre de las películas con mayor puntaje, en orden descendente.

- def recomendacion( titulo ): Se ingresa el nombre de una película y recomienda las similares en una lista de 5 valores.

## Por ultimo, se utiliza Render para poder realizar el deploy del proyecto e interactuar con las funciones realizadas