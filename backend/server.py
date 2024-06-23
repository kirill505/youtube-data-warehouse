import os

from fastapi import FastAPI
from src.yt_subs_parsing.parsing_yt_sub import fetch_youtube_subtitles
app = FastAPI()


@app.get('/')
def base():
    return "Hello world!"


@app.post("/youtube_link")
def get_youtube_link(yt_link: str):
    """Get youtube link"""
    root_dir = os.getenv("SAVE_PATH")
    print(root_dir)
    fetch_youtube_subtitles(yt_link, root_dir)

    return yt_link
