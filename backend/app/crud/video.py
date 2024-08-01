from sqlalchemy.orm import Session
from datetime import datetime
from app.models.video import Video
from app.models.channel import Channel
from app.models.video_stats import VideoStats
from app.schemas.video import VideoCreate, VideoUpdate
from app.schemas.video_stats import VideoStatsCreate
from app.youtube.client import YouTubeClient
from app.youtube.parser import parse_video_info
from app.youtube.parser import parse_channel_info
from app.core.config import settings
from app.crud.channel import get_channel, create_channel
from typing import List


def get_video(db: Session, video_id: str):
    return db.query(Video).filter(Video.video_id == video_id).first()

def create_video(db: Session, video_id: str):
    if get_video(db, video_id):
        raise ValueError("Video already exists")

    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    video_data = youtube_client.get_video_info(video_id)

    if not video_data["items"]:
        raise ValueError("Video not found on YouTube")

    video_info, stats = parse_video_info(video_data)

    # Check if the channel exists, if not, create it
    db_channel = get_channel(db, video_info.channel_id)
    if not db_channel:
        channel_data = youtube_client.get_channel_info(video_info.channel_id)
        if not channel_data["items"]:
            raise ValueError("Channel not found on YouTube")
        channel_info, channel_stats = parse_channel_info(channel_data)
        create_channel(db, channel_info)

    db_video = Video(
        video_id=video_info.video_id,
        channel_id=video_info.channel_id,
        title=video_info.title,
        description=video_info.description,
        published_at=video_info.published_at,
        last_updated_at=datetime.utcnow()
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def update_video(db: Session, video_id: str):
    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    video_data = youtube_client.get_video_info(video_id)

    if not video_data["items"]:
        raise ValueError("Video not found on YouTube")

    video_info, stats = parse_video_info(video_data)

    db_video = get_video(db, video_id)
    if not db_video:
        raise ValueError("Video not found")

    video_update = VideoUpdate(
        title=video_info.title,
        description=video_info.description,
        published_at=video_info.published_at,
        last_updated_at=datetime.utcnow()
    )

    for key, value in video_update.dict(exclude_unset=True).items():
        setattr(db_video, key, value)

    db.commit()
    db.refresh(db_video)
    return db_video


def delete_video(db: Session, video_id: str):
    db_video = db.query(Video).filter(Video.video_id == video_id).first()
    if db_video:
        db.delete(db_video)
        db.commit()
    return db_video


def create_video_stats(db: Session, video_stats: VideoStatsCreate):
    db_video_stats = VideoStats(
        video_id=video_stats.video_id,
        view_count=video_stats.view_count,
        like_count=video_stats.like_count,
        comment_count=video_stats.comment_count,
        last_updated_at=datetime.utcnow()
    )
    db.add(db_video_stats)
    db.commit()
    db.refresh(db_video_stats)
    return db_video_stats


def get_top_videos(db: Session, limit: int = 1) -> List[VideoCreate]:
    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    top_videos_data = youtube_client.get_top_videos(limit=limit)

    top_videos = []
    for video_data in top_videos_data['items']:
        video_info, stats = parse_video_info(video_data)

        if get_video(db, video_info.video_id):
            print("Video already exists")
            continue

        top_videos.append(video_info)

        # Check if the channel exists, if not, create it
        db_channel = get_channel(db, video_info.channel_id)
        if not db_channel:
            channel_data = youtube_client.get_channel_info(video_info.channel_id)
            if not channel_data["items"]:
                raise ValueError("Channel not found on YouTube")
            channel_info, channel_stats = parse_channel_info(channel_data)

            db_channel = Channel(
                channel_id=channel_info.channel_id,
                channel_name=channel_info.channel_name,
                description=channel_info.description,
                created_at=channel_info.created_at,
                last_updated_at=datetime.utcnow()
            )

            db.add(db_channel)
            db.commit()
            db.refresh(db_channel)

        db_video = Video(
            video_id=video_info.video_id,
            channel_id=video_info.channel_id,
            title=video_info.title,
            description=video_info.description,
            published_at=video_info.published_at,
            last_updated_at=datetime.utcnow()
        )
        db.add(db_video)
        db.commit()
        db.refresh(db_video)

        # create_video_stats(db=db, video_stats=stats)

    return top_videos
