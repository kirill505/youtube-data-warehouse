from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class VideoBase(BaseModel):
    video_id: str
    channel_id: str
    title: str
    description: Optional[str] = None
    published_at: datetime


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    last_updated_at: datetime

class VideoInDBBase(VideoBase):
    last_updated_at: datetime

    class Config:
        orm_mode = True

class Video(VideoInDBBase):
    pass

class VideoInDB(VideoInDBBase):
    pass
