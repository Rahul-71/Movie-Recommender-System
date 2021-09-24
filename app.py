# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 00:40:22 2021
"""
import streamlit as st
import pickle
import pandas as pd
import requests


movies = pickle.load(open('movie.pkl', 'rb'))     # movies is a dict
movie_df = pd.DataFrame(movies)    # re-creating as Dataframe from dictionary
similarity = pickle.load(open('similarity.pkl','rb'))

# to fetch the poster of a particular movie id
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d9b48f14f7d4c533ff9e040252581612")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

# to recommed the movie based on given movie title
def recommed(title):
    # try:
        movie_index = movie_df[movie_df['title']==title.lower()].index[0]
        # to fetch the top 5 similar movie title based on given movie
        similar_movie = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x:x[1])[1:6]
        print("similar movies are: ",similar_movie)
        recommended_movie = []
        recommended_movie_poster = []

        for i in similar_movie:
            movie_id = movie_df.iloc[i[0]]['id']
            movie_name = movie_df.iloc[i[0]]['title']
            recommended_movie.append(movie_name.title())
            recommended_movie_poster.append(fetch_poster(movie_id))
        return recommended_movie, recommended_movie_poster
    # except e:
    #     st.write(e.message())
    #     st.write('Please enter the valid movie name....')


st.title('Movie Recommendation System')

selected_movie = st.selectbox('Enter a name of movie....',
movie_df['title'].apply(lambda x:x.title()).values)

if st.button('Recommend'):
    # st.write(selected_movie)
    name, poster = recommed(selected_movie)
    # for i in name:
    #     st.write(i)

    st.title("Top 5 recommended movies ")
    cols = st.columns(5)

    for i, movie in enumerate(zip(name, poster)):
        with cols[i]:
            st.image(movie[1])
            st.text(movie[0])

