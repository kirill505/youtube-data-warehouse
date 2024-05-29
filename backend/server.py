from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def base():
    return "Hello world!"


@app.post("/youtube_link")
def get_youtube_link(yt_link: str):
    """Get youtube link"""

    return yt_link
