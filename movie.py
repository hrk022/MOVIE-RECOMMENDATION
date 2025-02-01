from datetime import date
import pickle
from urllib import response
import pandas as pd
import streamlit as st
import requests

movie_dict = pickle.load(open("recommendation.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
movie_dict = pd.DataFrame(movie_dict)
st.title("Movie recommender")

option = st.selectbox("Select a movie to get recommendations",movie_dict["title"].values)

def fetch(movies_id):
    url = f"https://api.themoviedb.org/3/movie/{movies_id}?api_key=d0a0841bb6ddaca5d079448679773385"
    response = requests.get(url)
    data = response.json()

    # Debugging: Print API response to check if poster_path exists
    print(f"Fetched data for movie ID {movies_id}: {data}")

    poster_path = data.get("poster_path")  # Safely get poster_path
    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path
    return None  # Return None if no poster is found



def recommended(movie):
    movie_index = movie_dict[movie_dict["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = []
    posters = []
    
    for i in movies_list:
        movie_id = movie_dict.iloc[i[0]]["movie_id"]
        movie_title = movie_dict.iloc[i[0]]["title"]
        poster_url = fetch(movie_id)  # Get the poster URL
        
        if poster_url:  # Only append if there's a valid poster URL
            posters.append(poster_url)
        
        recommended_movies.append(movie_title)
    
    return recommended_movies, posters  # Return both titles and posters




if st.button("Recommendation"):
    recommendations, posters = recommended(option)
    
    # Create the first row with 5 columns
    cols1 = st.columns(5)
    for col, movie, poster in zip(cols1, recommendations[:5], posters[:5]):
        with col:
            st.image(poster, caption=movie, use_column_width=True)
    
    # Create the second row with 5 columns
    cols2 = st.columns(5)
    for col, movie, poster in zip(cols2, recommendations[5:], posters[5:]):
        with col:
            st.image(poster, caption=movie, use_column_width=True)
