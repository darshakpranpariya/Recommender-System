import streamlit as st
import os
import openai
import requests

st.title('Recommendation Based On Description')

def fetch_poster(movie_name):
    url =f''' https://api.themoviedb.org/3/search/movie?api_key=8265bd1679663a7ea12ac168da84d2e8&query=${movie_name}'''
    data = requests.get(url)
    data = data.json()
    try:
        poster_path = data['results'][0]['poster_path']
    except:
        return ''
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def get_recommendation(text):
    openai.api_key = "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"

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt=text,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    )
    return response['choices'][0]['text']

title = st.text_area('Enter a little description of movie over here...',placeholder='Want to watch movies that have...')


if st.button('Show Recommendation'):
    title = 'want to watch movies that have ' + title + ', give name only by commas seperated?'
    list_of_movies = get_recommendation(title)
    list_of_movies = list_of_movies.split(',')
    rows = [st.columns(5) for _ in range(len(list_of_movies)//5)]
    cols = [column for row in rows for column in row]
    if(len(list_of_movies) > 0):
        for i, x in enumerate(cols):
            path = fetch_poster(list_of_movies[i])
            if(path != ''):
                with x: 
                    st.text(list_of_movies[i])
                    st.image(path)
            else:
                st.header('Sorry, we couldn\'t find any movies with this description!')
    else:
        st.header('Sorry, we couldn\'t find any movies with this description!')

