import aiohttp
from app.youtube.client import YouTubeClient
from app.youtube.parser import parse_video_info, parse_channel_info
from app.core.config import settings
from app.schemas.video import VideoCreate
from datetime import datetime


async def fetch_video_info(video_id: str):
    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    video_data = await youtube_client.get_video_info(video_id)

    if not video_data["items"]:
        raise ValueError("Video not found on YouTube")

    return await parse_video_info(video_data["items"][0])


async def fetch_channel_info(channel_id: str):
    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    channel_data = await youtube_client.get_channel_info(channel_id)
    if not channel_data["items"]:
        raise ValueError("Channel not found on YouTube")

    return await parse_channel_info(channel_data["items"][0])


async def fetch_top_videos(regioncode: str, limit: int = 200):
    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    top_videos_data = await youtube_client.get_top_videos(regioncode=regioncode, limit=limit)
    top_videos = []
    for video_data in top_videos_data:
        video_info, stats = await parse_video_info(video_data)
        top_videos.append(video_info)

    return top_videos


async def search_videos(query: str, limit: int = 200):
    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    search_results = await youtube_client.search_videos(query, limit)
    videos = []

    for video_data in search_results:
        print(video_data)
        # video_info, _ = await parse_video_info(video_data)
        published_at = datetime.strptime(video_data["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
        video_info = VideoCreate(
            video_id=video_data["id"]["videoId"],  # Добавляем video_id
            channel_id=video_data["snippet"]["channelId"],
            title=video_data["snippet"]["title"],
            description=video_data["snippet"].get("description", ""),
            published_at=published_at
        )
        print("Parsed video data:", video_info)  # Отладочное сообщение
        videos.append(video_info)

    return videos
