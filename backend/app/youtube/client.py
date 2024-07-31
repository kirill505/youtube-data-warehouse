from googleapiclient.discovery import build
from app.core.config import settings


class YouTubeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = build("youtube", "v3", developerKey=self.api_key)

    def get_channel_info(self, channel_id: str):
        request = self.client.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        return response

    def get_video_info(self, video_id: str):
        request = self.client.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()
        return response
