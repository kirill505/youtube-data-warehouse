from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelUpdate
from app.utils.youtube_service import fetch_video_info, fetch_top_videos, fetch_channel_info
from sqlalchemy.future import select
from app.utils.datetime_utils import remove_timezone


async def get_channel(db: AsyncSession, channel_id: str):
    result = await db.execute(select(Channel).filter(Channel.channel_id == channel_id))

    return result.scalars().first()

async def create_new_channel(db: AsyncSession, channel_id: str):
    channel_info, _ = await fetch_channel_info(channel_id)
    db_video = await create_channel(db, channel_info)
    return db_video


async def create_channel(db: AsyncSession, channel: ChannelCreate):
    db_channel = await get_channel(db, channel.channel_id)
    if db_channel:
        raise ValueError("Channel already exists")

    db_channel = Channel(
        channel_id=channel.channel_id,
        channel_name=channel.channel_name,
        description=channel.description,
        created_at=remove_timezone(channel.created_at),
        last_updated_at=remove_timezone(datetime.now(timezone.utc))
    )

    db.add(db_channel)
    await db.commit()
    await db.refresh(db_channel)

    return db_channel


async def update_channel(db: AsyncSession, channel_id: str, channel_update: ChannelUpdate):
    db_channel = await get_channel(db, channel_id)
    if db_channel is None:
        return None

    update_data = channel_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_channel, key, value)
    db_channel.last_updated_at = remove_timezone(datetime.now(timezone.utc))

    await db.commit()
    await db.refresh(db_channel)
    return db_channel
