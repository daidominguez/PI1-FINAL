# **PI_ML-OPS**

**Daineth Dominguez FT-11**

---
Como parte de un equipo de  **`Data Scientist`** de una start-up que provee servicios de agregación de plataformas de streaming, se llevará a cabo un modelo de ML para un sistema de recomendación de peliculas que aún no se ha puesto en marcha. 

Debido a la poca madurez de los datos, se realiza primero una limpieza rapida de los mismos para llevar a cabo consultas sobre los registros a traves de una API. Luego pasamos a un análisis exploratorio de los datos (EDA) para determinar relación entre variables, determinar anomalías, y ver si hay algún patrón interesante para explorar en el proceso de ML.

Por ultimo, entrenamos un modelo de machine learning para armar un sistema de recomendación de películas a los usuarios basándose en películas similares.

---
## ETL

Para el proceso de ETL, se utilizó python como herramienta para manejar los datasets administrados por el cliente. Las transformaciones se realizaron en el siguiente orden:
  - Importacion de las librerias y datasets para el tratamiento de datos.
  - Revision de las columnas `title` y `id` para determinar errores en las mismas.
  - Eliminacion de columnas irrelevantes para el estudio.
  - Creación de una columna llamada `return` que relaciona `revenue y budget`. 
  - Tratamiento de la columna `release_date` para crear una nueva llamada `release_year`.
  - Desanidación de las columnas `belongs_to_collection, genres, production_companies, production_countries, spoken_languages, cast y crew`, dejando únicamentes el director de la pelicula de la columna `crew` y los primeros 5 actores de la columna `cast`. 
  - Exportamos el archivo con las columnas requeridas para realizar las primeras consultas en la API, llamandolo `df_API.csv`.
    
---
## Desarrollo API

Para la creación de la api, se creó un entorno virtual de Python llamado `venv`, y se trabajaron las consultas con el modulo de fastAPI, el mismo permite crear una plataforma por medio del servidor Render, que trabaja bajo sistema HTTP simples.Las consultas que se pueden realizar son las siguientes: 
- def **cantidad_filmaciones_mes(Mes)**:
    Se ingresa un mes en idioma español y devuelve la cantidad de películas que fueron estrenadas en el mes consultado.

- def **cantidad_filmaciones_dia(Dia)**:
    Se ingresa un día en idioma español y devuelve la cantidad de películas que fueron estrenadas en el día consultado.

- def **score_titulo(titulo_de_la_filmación)**:
    Se ingresa el título de una filmación y devuelve el título, año de estreno y score del mismo.

- def **votos_titulo(titulo_de_la_filmación)**:
    Se ingresa el título de una filmación y devuelve el título, la cantidad de votos y el valor promedio de las votaciones si la filmación cuenta con al menos 2000 valoraciones, en caso contrario, muestra un mensaje avisando que no cumple la condición.

- def **get_actor( nombre_actor)**:
    Se ingresa el nombre de un actor y devuelve el éxito del mismo medido a través del retorno. Además, la cantidad de películas que las que ha participado y el promedio de retorno de cada una.

- def **get_director(nombre_director)**:
    Se ingresa el nombre de un director y devuelve el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

---
## EDA

En esta etapa hacemos un analisis mas detallado del dataset, evaluando posibles anomalías en cada columna o datos de interés para aplicar el modelo de Machine Learning. El proceso se siguió en el siguiente orden:
- Eliminacion de la columna `release_date` ya una vez creada la columna `release_year` que es mas relevante.
- Evaluacion de las variables de mayor interés para el modelo, como `original_language`, `spoken_languages`, `overview`, `status` y `tagline`. Se completaron valores faltantes analizando relación entre las mismas y transformaciones de los datos para facilitar el proceso de ML. Se pudo observar por ejemplo que habían registros que estaban marcados como cancelado, rumorado o vacíos que se pueden descartar para el modelo.
- Graficos de distribucion para las columnas relacionadas con puntuación de las peliculas como `vote_average` , `vote_count` y `popularity`, donde se pudo observar que la mayoria de las valoraciones nulas se referian a peliculas muy antiguas, y que ademas existe una relacion directa entre la cantidad de votos y la popularidad. 
-  Analisis de las columnas `runtime` y `release_year`. Dato importante para el modelo debido a que muchas peliculas marcadas con duracion nula correspondian a peliculas que no fueron estrenadas y por lo tanto no tiene sentido utilizarlas para el sistema de recomendación.
- Por ultimo, se tomó como muestra representativa las peliculas couya votacion es superior a 150, con duracion distinta de cero. Como atributos relevantes para el sistema de recomendación se consideraron las columnas `title`,`genres`,`overview`,`tagline`,`cast`, `crew`.

---
## Sistema de recomendación.

Una vez realizado el proceso de ETL y EDA, pasamos al sistema de recomendación. Con los datos limpios y un análisis adecuado de la información que se obtuvo de los datasets, se creó un modelo supervisado aplicado a una muestra representativa, que de acuerdo a la similitud entre variables categoricas de cada pelicula y utilizando el modelo `cosine_similarity` se pudo determinar las 5 peliculas con mayor relación con respecto a la película consultada por el usuario.

Una vez creado el modelo se realiza una funcion que pueda ser consultada a traves de la API por el usuario.
  
---
## Video.

En el siguiente [enlace](https://youtu.be/k7bFVW58ENw)  se encuentra un video expositivo del proyecto y los procesos realizados para lograr satisfacer las consultas requeridas.

## Enlaces. 

- [Base de datos](https://drive.google.com/drive/folders/1TNTiiR4iUpjESXhZxgfBVi2hwYy9nLOI?usp=sharing) <br>
- [API](https://movies-services.onrender.com/docs)
