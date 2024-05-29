import io
import requests
import streamlit as st


# interact with FastAPI endpoint
backend = "http://fastapi:8000/youtube_link"


def process(image):

    return backend


# construct UI layout
st.title("LinguaSpark")

st.write(
    """Ignite your language learning with LinguaSpark. Share YouTube videos 
        and receive personalized lessons on vocabulary, grammar, and pronunciation
    """
)

title = st.text_input("youtube video link:", "put here")

if st.button("get subtitles"):

    col1, col2 = st.columns(2)

