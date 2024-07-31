from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any
from app.schemas.channel import Channel, ChannelCreate, ChannelUpdate
from app.crud import channel as crud_channel
from app.crud import channel_stats as crud_channel_stats
from app.db.session import get_db
from app.youtube.client import YouTubeClient
from app.youtube.parser import parse_channel_info
from app.core.config import settings
from app import crud

router = APIRouter()

@router.post("/", response_model=ChannelCreate)
async def create_channel(
        channel_id: str,  # Изменено на URL канала
        db: Session = Depends(get_db)
) -> Any:

    db_channel = crud_channel.get_channel(db, channel_id)
    if db_channel:
        raise HTTPException(status_code=400, detail="Channel already exists")

    # youtube_client = YouTubeClient(settings.YOUTUBE_API_KEY)
    # data = youtube_client.get_channel_info(channel_id)
    # channel_info, stats = parse_channel_info(data)

    # new_channel = crud_channel.create_channel(db, channel_info)
    try:
        new_channel = crud.channel.create_channel(db, channel_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # crud_channel_stats.create_channel_stats(db, stats)

    return new_channel

@router.put("/{channel_id}", response_model=Channel)
async def update_channel(
        channel_id: str,
        db: Session = Depends(get_db)
) -> Any:
    try:
        updated_channel = crud.channel.update_channel(db, channel_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return updated_channel