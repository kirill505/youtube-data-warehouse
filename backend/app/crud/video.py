import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models.video import Video
from app.models.channel import Channel
from app.models.video_stats import VideoStats
from app.schemas.video import VideoCreate, VideoUpdate
from app.schemas.video_stats import VideoStatsCreate
from app.crud.channel import get_channel, create_channel, create_new_channel
from app.utils.youtube_service import fetch_video_info, fetch_top_videos, fetch_channel_info, search_videos
from typing import List, Awaitable, Dict
from sqlalchemy.future import select
from app.utils.datetime_utils import remove_timezone
import time
from app.db.session import SessionLocal


async def get_video(db: AsyncSession, video_id: str):
    result = await db.execute(select(Video).filter(Video.video_id == video_id))
    return result.scalars().first()

async def create_new_video_and_channel(db: AsyncSession, video_info: VideoCreate):
    async with db.begin():  # Использование транзакции
        # Проверка существования канала
        db_channel = await get_channel(db, video_info.channel_id)
        print(f"Channel {video_info.channel_id} found: {db_channel}")

        if not db_channel:
            channel_info, _ = await fetch_channel_info(video_info.channel_id)
            print(f"Creating new channel: {channel_info}")
            db_channel = Channel(
                channel_id=channel_info.channel_id,
                channel_name=channel_info.channel_name,
                description=channel_info.description,
                created_at=remove_timezone(channel_info.created_at),
                last_updated_at=remove_timezone(datetime.now(timezone.utc))
            )
            db.add(db_channel)

        # Проверка существования видео
        db_video = await get_video(db, video_info.video_id)
        print(f"Video {video_info.video_id} found: {db_video}")

        if not db_video:
            db_video = Video(
                video_id=video_info.video_id,
                channel_id=video_info.channel_id,
                title=video_info.title,
                description=video_info.description,
                published_at=video_info.published_at,
                last_updated_at=remove_timezone(datetime.now(timezone.utc))
            )
            db.add(db_video)

    await db.commit()  # Коммит транзакции
    return db_video, db_channel


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


async def create_video_task(video_info):
    async with SessionLocal() as db:
        try:
            await create_new_video_and_channel(db, video_info)
        except Exception as e:
            await db.rollback()
            print(f"Error creating video {video_info.video_id} or channel {video_info.channel_id}: {e}")
        else:
            await db.commit()


async def process_videos(video_queue: asyncio.Queue):
    while not video_queue.empty():
        video_info = await video_queue.get()
        print(f"Processing video: {video_info.video_id}")
        await create_video_task(video_info)
        video_queue.task_done()


async def write_pool_data_to_db_async(top_videos_data: List[VideoCreate]):
    top_videos = []
    video_queue = asyncio.Queue()
    chunk_size = 200

    for video_info in top_videos_data:
        top_videos.append(video_info)
        await video_queue.put(video_info)

    # Запуск нескольких воркеров для обработки очереди видео
    workers = [asyncio.create_task(process_videos(video_queue)) for _ in range(chunk_size)]
    await video_queue.join()  # Ожидание завершения всех задач
    for worker in workers:
        worker.cancel()  # Завершение воркеров

    return top_videos


async def get_top_videos(regioncode: str, limit: int = 200) -> List[VideoCreate]:
    start_time = time.perf_counter()

    top_videos_data = await fetch_top_videos(regioncode = regioncode, limit=limit)
    top_videos = await write_pool_data_to_db_async(top_videos_data)

    end_time = time.perf_counter()
    total_time = end_time - start_time
    print('Finished for: ' + str(total_time) + ' seconds')

    return top_videos


async def search_and_store_videos(db: AsyncSession, query: str, limit: int = 200) -> List[VideoCreate]:
    search_results = await search_videos(query, limit)
    return await write_pool_data_to_db_async(search_results)
