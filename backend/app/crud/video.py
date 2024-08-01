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
from app.crud.channel import get_channel, create_channel, create_new_channel
from app.utils.youtube_service import fetch_video_info, fetch_top_videos, fetch_channel_info
from typing import List


def get_video(db: Session, video_id: str):
    return db.query(Video).filter(Video.video_id == video_id).first()

def create_new_video(db: Session, video_id: str):
    video_info, stats = fetch_video_info(video_id)

    # Check if the channel exists, if not, create it
    db_channel = get_channel(db, video_info.channel_id)
    if not db_channel:
        channel_info, _ = fetch_channel_info(video_info.channel_id)
        create_channel(db, channel_info)

    db_video = create_video(db, video_info)
    return db_video


def create_video(db: Session, video: VideoCreate):
    if get_video(db, video.video_id):
        raise ValueError("Video already exists")

    db_video = Video(
        video_id=video.video_id,
        channel_id=video.channel_id,
        title=video.description,
        published_at=video.published_at,
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
    top_videos_data = fetch_top_videos(limit=15)
    top_videos = []

    for video_info in top_videos_data:
        try:
            if not get_video(db, video_info.video_id):
                top_videos.append(video_info)

                db_channel = get_channel(db, video_info.channel_id)
                if not db_channel:
                    channel_info, _ = fetch_channel_info(video_info.channel_id)
                    create_channel(db, channel_info)
                create_video(db, video_info)

                # create_video_stats(db=db, video_stats=stats)
        except ValueError as e:
            print(f"Skipping video {video_info.video_id}: {e}")
    return top_videos
