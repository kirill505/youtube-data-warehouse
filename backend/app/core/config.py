import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY")


settings = Settings()
