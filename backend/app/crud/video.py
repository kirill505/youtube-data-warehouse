from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models.video import Video
from app.models.video_stats import VideoStats
from app.schemas.video import VideoCreate, VideoUpdate
from app.schemas.video_stats import VideoStatsCreate
from app.crud.channel import get_channel, create_channel, create_new_channel
from app.utils.youtube_service import fetch_video_info, fetch_top_videos, fetch_channel_info
from typing import List
from sqlalchemy.future import select
from app.utils.datetime_utils import remove_timezone


async def get_video(db: AsyncSession, video_id: str):
    result = await db.execute(select(Video).filter(Video.video_id == video_id))
    return result.scalars().first()

async def create_new_video(db: AsyncSession, video_id: str):
    video_info, stats = await fetch_video_info(video_id)

    # Check if the channel exists, if not, create it
    db_channel = await get_channel(db, video_info.channel_id)
    if not db_channel:
        channel_info, _ = await fetch_channel_info(video_info.channel_id)
        await create_channel(db, channel_info)

    db_video = await create_video(db, video_info)
    return db_video


async def create_video(db: AsyncSession, video: VideoCreate):
    if await get_video(db, video.video_id):
        raise ValueError("Video already exists")

    db_video = Video(
        video_id=video.video_id,
        channel_id=video.channel_id,
        title=video.description,
        published_at=video.published_at,
        last_updated_at=remove_timezone(datetime.now(timezone.utc))
    )
    db.add(db_video)
    await db.commit()
    await db.refresh(db_video)
    return db_video


async def update_video(db: AsyncSession, video_id: str):
    video_info, stats = await fetch_video_info(video_id)

    db_video = await get_video(db, video_id)
    if not db_video:
        raise ValueError("Video not found")

    video_update = VideoUpdate(
        title=video_info.title,
        description=video_info.description,
        published_at=video_info.published_at,
        last_updated_at=remove_timezone(datetime.now(timezone.utc))
    )

    for key, value in video_update.dict(exclude_unset=True).items():
        setattr(db_video, key, value)

    await db.commit()
    await db.refresh(db_video)
    return db_video


async def delete_video(db: AsyncSession, video_id: str):
    db_video = await get_video(db, video_id)
    if db_video:
        await db.delete(db_video)
        await db.commit()
    return db_video


async def create_video_stats(db: AsyncSession, video_stats: VideoStatsCreate):
    db_video_stats = VideoStats(
        video_id=video_stats.video_id,
        view_count=video_stats.view_count,
        like_count=video_stats.like_count,
        comment_count=video_stats.comment_count,
        last_updated_at=remove_timezone(datetime.now(timezone.utc))
    )
    db.add(db_video_stats)
    await db.commit()
    await db.refresh(db_video_stats)
    return db_video_stats


async def get_top_videos(db: AsyncSession, limit: int = 1) -> List[VideoCreate]:
    top_videos_data = await fetch_top_videos(limit=15)
    top_videos = []

    for video_info in top_videos_data:
        try:
            if not await get_video(db, video_info.video_id):
                top_videos.append(video_info)

                db_channel = await get_channel(db, video_info.channel_id)
                if not db_channel:
                    channel_info, _ = await fetch_channel_info(video_info.channel_id)
                    await create_channel(db, channel_info)
                await create_video(db, video_info)

                # create_video_stats(db=db, video_stats=stats)
        except ValueError as e:
            print(f"Skipping video {video_info.video_id}: {e}")
    return top_videos
