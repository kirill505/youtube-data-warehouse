from sqlalchemy.orm import Session
from datetime import datetime
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelUpdate
from app.youtube.client import YouTubeClient
from app.youtube.parser import parse_channel_info
from app.core.config import settings


def get_channel(db: Session, channel_id: str):
    return db.query(Channel).filter(Channel.channel_id == channel_id).first()

def create_channel(db: Session, channel_id: str):
    db_channel = get_channel(db, channel_id)
    if db_channel:
        raise ValueError("Channel already exists")

    youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    data = youtube_client.get_channel_info(channel_id)
    if not data["items"]:
        raise ValueError("Channel not found")

    channel_info, stats = parse_channel_info(data)

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
