from pydantic import BaseModel
from datetime import datetime

class VideoStatsBase(BaseModel):
    video_id: str
    view_count: int
    like_count: int
    comment_count: int


class VideoStatsCreate(VideoStatsBase):
    last_updated_at: datetime


class VideoStats(VideoStatsBase):
    id: int
    last_updated_at: datetime

    class Config:
        orm_mode = True
