import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models.video import Video
from app.models.video_stats import VideoStats
from app.schemas.video import VideoCreate, VideoUpdate
from app.schemas.video_stats import VideoStatsCreate
from app.crud.channel import get_channel, create_channel, create_new_channel
from app.utils.youtube_service import fetch_video_info, fetch_top_videos, fetch_channel_info
from typing import List, Awaitable, Dict
from sqlalchemy.future import select
from app.utils.datetime_utils import remove_timezone
import time
from app.db.session import SessionLocal


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
        title=video.title,
        description=video.description,
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


async def create_channel_task(channel_info):
    async with SessionLocal() as db:
        try:
            await create_channel(db, channel_info)
        except Exception as e:
            await db.rollback()
            print(f"Error creating channel {channel_info.channel_id}: {e}")
        else:
            await db.commit()


async def create_video_task(video_info):
    async with SessionLocal() as db:
        try:
            await create_video(db, video_info)
        except Exception as e:
            await db.rollback()
            print(f"Error creating video {video_info.video_id}: {e}")
        else:
            await db.commit()


async def execute_tasks_in_chunks(tasks: List[Awaitable], chunk_size: int):
    for i in range(0, len(tasks), chunk_size):
        chunk = tasks[i:i + chunk_size]
        print(len(chunk))
        await asyncio.gather(*chunk)


async def process_videos(video_queue: asyncio.Queue):
    while not video_queue.empty():
        video_info = await video_queue.get()
        await create_video_task(video_info)
        video_queue.task_done()


async def write_pool_data_to_db_async(top_videos_data: List[VideoCreate]):
    top_videos = []
    video_queue = asyncio.Queue()
    chunk_size = 200

    for video_info in top_videos_data:
        try:
            async with SessionLocal() as db:
                if not await get_video(db, video_info.video_id):
                    top_videos.append(video_info)
                    db_channel = await get_channel(db, video_info.channel_id)
                    if not db_channel:
                        channel_info, _ = await fetch_channel_info(video_info.channel_id)
                        await create_channel_task(channel_info)
                    await video_queue.put(video_info)
        except ValueError as e:
            print(f"Skipping video {video_info.video_id}: {e}")

    # Запуск нескольких воркеров для обработки очереди видео
    workers = [asyncio.create_task(process_videos(video_queue)) for _ in range(chunk_size)]
    await video_queue.join()  # Ожидание завершения всех задач
    for worker in workers:
        worker.cancel()  # Завершение воркеров

    return top_videos


async def get_top_videos(limit: int = 50) -> List[VideoCreate]:
    start_time = time.perf_counter()

    top_videos_data = await fetch_top_videos(limit=limit)
    top_videos = await write_pool_data_to_db_async(top_videos_data)

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print('Finished for: ' + str(total_time) + ' seconds')

    return top_videos
