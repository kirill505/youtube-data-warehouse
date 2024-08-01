from sqlalchemy.orm import Session
from datetime import datetime
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelUpdate
from app.utils.youtube_service import fetch_video_info, fetch_top_videos, fetch_channel_info


def get_channel(db: Session, channel_id: str):
    return db.query(Channel).filter(Channel.channel_id == channel_id).first()


def create_new_channel(db: Session, channel_id: str):
    channel_info, _ = fetch_channel_info(channel_id)

    db_video = create_channel(db, channel_info)
    return db_video


def create_channel(db: Session, channel: ChannelCreate):
    db_channel = get_channel(db, channel.channel_id)
    if db_channel:
        raise ValueError("Channel already exists")

    db_channel = Channel(
        channel_id=channel.channel_id,
        channel_name=channel.channel_name,
        description=channel.description,
        created_at=channel.created_at,
        last_updated_at=datetime.utcnow()
    )

    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)

    return db_channel

def update_channel(db: Session, channel_id: str, channel_update: ChannelUpdate):
    db_channel = get_channel(db, channel_id)
    if db_channel is None:
        return None

    update_data = channel_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_channel, key, value)
    db_channel.last_updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_channel)
    return db_channel
