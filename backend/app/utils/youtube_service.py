import aiohttp
from app.youtube.client import YouTubeClient
from app.youtube.parser import parse_video_info, parse_channel_info
from app.core.config import settings


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


async def fetch_top_videos(limit: int = 50):
    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    top_videos_data = await youtube_client.get_top_videos(limit=limit)
    top_videos = []
    for video_data in top_videos_data['items']:
        video_info, stats = await parse_video_info(video_data)

        top_videos.append(video_info)

    return top_videos
