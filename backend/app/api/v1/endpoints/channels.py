from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from app.schemas.channel import Channel, ChannelCreate, ChannelUpdate
from app.crud import channel as crud_channel
from app.db.session import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=ChannelCreate)
async def create_channel(
        channel_id: str,  # Изменено на URL канала
        db: AsyncSession = Depends(get_db)
) -> Any:

    db_channel = await crud_channel.get_channel(db, channel_id)
    if db_channel:
        raise HTTPException(status_code=400, detail="Channel already exists")

    try:
        new_channel = await crud.channel.create_new_channel(db, channel_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_channel

@router.put("/{channel_id}", response_model=Channel)
async def update_channel(
        channel_id: str,
        db: AsyncSession = Depends(get_db)
) -> Any:
    try:
        updated_channel = await crud.channel.update_channel(db, channel_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return updated_channel
