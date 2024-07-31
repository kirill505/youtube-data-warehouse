from pydantic import BaseModel
from datetime import datetime


class ChannelStatsBase(BaseModel):
    channel_id: str
    subscriber_count: int
    video_count: int
    view_count: int


class ChannelStatsCreate(ChannelStatsBase):
    last_updated_at: datetime


class ChannelStats(ChannelStatsBase):
    id: int
    last_updated_at: datetime

    class Config:
        orm_mode = True
