import io
import requests
import streamlit as st


# interact with FastAPI endpoint
backend = "http://backend:8000/youtube_link/"


def process(server_url: str, url: str):
    r = requests.post(
        server_url, data={'yt_link': url}, headers={"Content-Type": "application/json"}
    )
    return r


# construct UI layout
st.title("LinguaSpark")

st.write(
    """Ignite your language learning with LinguaSpark. Share YouTube videos 
        and receive personalized lessons on vocabulary, grammar, and pronunciation
    """
)

yt_link = st.text_input("youtube video link:", "put here")

if st.button("get subtitles"):

    col1, col2 = st.columns(2)

    res = process(backend, yt_link)
    if yt_link and res.status_code:
        st.status(f"youtube link has been uploaded")

