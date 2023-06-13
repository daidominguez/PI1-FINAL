import pandas as pd
import numpy as np 
import sklearn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

data= pd.read_csv(r'movie_list.csv', sep = ',', encoding='utf8')

cv = TfidfVectorizer(max_features=1000, stop_words='english')
vectorized_data = cv.fit_transform(data['tags'].values)
vectorized_dataframe = pd.DataFrame(vectorized_data.toarray(), index=data['tags'].index.tolist())
svd=TruncatedSVD(n_components=800)
reduced_data = svd.fit_transform(vectorized_dataframe)
reduced_data = svd.fit_transform(vectorized_dataframe)
similarity = cosine_similarity(reduced_data)

def modelo(titulo:str):
    movie=titulo.strip()
    recommend=[]
    movie_index = data[data['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:6]
    for i in movies_list:
        recommend.append(data.iloc[i[0]]['title'])
    return {'lista recomendada': recommend}