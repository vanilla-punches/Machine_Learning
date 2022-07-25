import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = 'f3f49cdadd2a2f530cb252fd361a7357'

def get_recommendations(title):
    idx = movies[movies['title'] == title].index[0] # Return index value from a movie name based on data
    
    sim_scores = list(enumerate(cosine_sim[idx])) # Return (idx, similarity)
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True) # Ascending by cosine similarity
    
    sim_scores = sim_scores[1:11]
    
    movie_indices = [i[0] for i in sim_scores]

    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id)

        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'

        images.append(image_path)
        titles.append(details['title'])
    
    return images, titles

movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide')
st.header('vanillaflix')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you like', movie_list)
if st.button('Recommend'):
    with st.spinner('Please wait...'):
        images, titles = get_recommendations(title)

        idx = 0
        for i in range(0, 2):
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1