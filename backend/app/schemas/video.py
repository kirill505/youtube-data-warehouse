from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    published_at: datetime

class VideoCreate(VideoBase):
    video_id: str
    channel_id: str
    title: str
    description: Optional[str] = None
    published_at: datetime


class VideoUpdate(VideoBase):
    last_updated_at: datetime

class VideoInDBBase(VideoBase):
    video_id: str
    channel_id: str
    last_updated_at: datetime

    class Config:
        orm_mode = True

class Video(VideoInDBBase):
    pass

class VideoInDB(VideoInDBBase):
    pass
