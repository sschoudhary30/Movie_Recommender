import streamlit as st

import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=5c01c93b0885e84bd0d42b73369c11bf&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names,recommended_movie_posters


st.title('Movie Recommender System 🎥')

#select_movie = st.selectbox(
    #'Which movie would you like to find?',
    #movies['title'].values)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

# pip install streamlit , for enviroment // python -m venv .venv,  .venv\Scripts\Activate.ps1,streamlit run app.py