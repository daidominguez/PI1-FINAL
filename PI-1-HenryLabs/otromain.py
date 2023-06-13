from fastapi import FastAPI, Path, UploadFile, File
import pandas as pd
import numpy as np 
from starlette.responses import RedirectResponse

app=FastAPI()
app.title="Mi Aplicacion con FastAPI"
app.description="Consultas basadas en el registro de peliculas de TMDB (The Movies DataBase)"
app.version="0.0.1"

data_movies = pd.read_csv(r'df_API.csv', sep = ',', encoding='utf8')
#data= pd.read_csv(r'movie_list.csv', sep = ',', encoding='utf8')

@app.get('/cantidad_filmaciones_mes/{Mes}', tags=['movies'])
async def cantidad_filmaciones_mes(Mes:str):
    mes=Mes.strip().lower()
    dict_meses = {
                'enero': 1,
                'febrero': 2,
                'marzo': 3,
                'abril': 4,
                'mayo': 5,
                'junio': 6,
                'julio': 7,
                'agosto': 8,
                'septiembre': 9,
                'octubre': 10,
                'noviembre': 11,
                'diciembre': 12
                }
    if mes not in (dict_meses.keys()):
        return 'No se reconoce el mes ingresado. Intenta escribirlo nuevamente verificando que esté escrito en español'
    else:    
        df_month= data_movies[['release_date']]
        df_month['release_date']=pd.to_datetime(df_month['release_date']).dt.month
        count = df_month[df_month['release_date']==dict_meses[mes]].value_counts()
        count=int(count)
        return  {'mes':Mes, 'cantidad':count}
    

@app.get('/cantidad_filmaciones_dia{Dia}', tags=['movies'])
async def cantidad_filmaciones_dia(Dia:str):
  dia=Dia.strip().lower()
  dict_dias={
    'lunes': 0,
    'martes': 1,
    'miércoles': 2,
    'miercoles': 2,
    'jueves': 3,
    'viernes': 4,
    'sábado': 5,
    'sabado': 5,
    'domingo': 6
    }
  if dia not in (dict_dias.keys()): return 'No se reconoce el dia ingresado. Intenta escribirlo nuevamente verificando que esté escrito en español'
  else:
    df_day= data_movies[['release_date']]
    df_day['release_date']=pd.to_datetime(df_day['release_date']).dt.weekday
    count = df_day[df_day['release_date']==dict_dias[dia]].value_counts()
    count=int(count)
    return {'dia':Dia, 'cantidad':count}
   
@app.get('/score_titulo/{Titulo}', tags=['movies'])
async def score_titulo(Titulo:str):
    titulo=Titulo.strip()
    data_movies['title'].astype(str)
    mask=data_movies['title']==titulo
    df=data_movies[mask][['title','popularity','release_year']]
    if df.empty: return 'No se reconoce la pelicula ingresada. Intenta escribirlo nuevamente'
    else:
        for indice, fila in df.iterrows():
            score=fila['popularity']
            year=fila['release_year']
    return {'titulo':Titulo, 'anio':year, 'popularidad':score} 
    
@app.get('/votos_titulo/{Titulo}', tags=['movies'])
async def votos_titulo(Titulo:str):
    titulo=Titulo.strip()
    data_movies['title'].astype(str)
    mask=data_movies['title']==titulo
    df=data_movies[mask][['title','vote_count','release_year','vote_average']]
    if df.empty: return 'No se reconoce la pelicula ingresada. Intenta escribirlo nuevamente'
    else:
        peliculas={}
        peliculas['titulo']=Titulo
        votes=[]
        years=[]
        avg=[]
        for indice, fila in df.iterrows():
            vote=fila['vote_count']
            if (vote>2000):
                votes.append(vote)
                years.append(int(fila['release_year']))
                avg.append(round(fila['vote_average'],1))
        peliculas['anio']=years
        peliculas['voto_total']=votes
        peliculas['voto_promedio']=avg
        if (votes==[]): return f'La pelicula {Titulo} no cumple con la cantidad minima de valoraciones requerida'
        else: return peliculas
                 
@app.get('/get_actor/{Actor}', tags=['movies'])
async def get_actor(Actor:str):
    name=Actor.strip()
    cadena_texto=data_movies['cast'].astype(str)
    encontrado=cadena_texto.str.contains(name, case=False)
    df_actor = data_movies[encontrado][['return']]
    if df_actor.empty: return 'No se reconoce el actor ingresado. Intenta escribirlo nuevamente'
    else:
        count_films=df_actor.shape[0]
        avg_film=round(df_actor['return'].mean(),2)
        sum_return=round(df_actor['return'].sum(),2)
        return {'actor':Actor, 'cantidad_filmaciones':count_films, 'retorno_total':sum_return, 'retorno_promedio':avg_film}

 
@app.get('/get_director/{Director}', tags=['movies'])
async def get_director(Director:str):
    name=Director.strip()
    cadena_texto=data_movies['crew'].astype(str)
    encontrado=cadena_texto.str.contains(name, case=False)
    df_director= data_movies[encontrado][['title','release_year','return','revenue','budget']]
    if df_director.empty: return 'No se reconoce el director ingresado. Intenta escribirlo nuevamente'
    else:
        peliculas={}
        df_director['revenue'].astype(float)
        df_director['budget'].astype(int)
        df_director['return'].astype(float)
        sum_return=round(df_director['return'].sum(),2)
        peliculas['director']=Director
        peliculas['retorno_total_director']=sum_return
        titulo=[]
        anio=[]
        costo=[]
        retorno=[]
        ganancia=[]
        for indice, fila in df_director.iterrows():
            titulo.append(fila['title'])
            anio.append(fila['release_year'])
            retorno.append(round(fila['return'],2))
            costo.append(fila['budget'])
            ganancia.append(fila['revenue'])  
        peliculas['peliculas']=titulo
        peliculas['anio']=anio
        peliculas['retorno_pelicula']=retorno
        peliculas['budget_pelicula']=costo
        peliculas['revenue_pelicula']=ganancia
        return peliculas

#from model import modelo
'''
@app.get('/recomendacion/{titulo}', tags=['movies'])
async def recomendacion(titulo:str):
    respuesta=modelo(titulo)
    return respuesta
'''