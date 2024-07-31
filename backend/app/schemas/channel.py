from pydantic import BaseModel
from datetime import datetime

class ChannelBase(BaseModel):
    channel_name: str
    description: str
    created_at: datetime

class ChannelCreate(ChannelBase):
    channel_id: str


class ChannelUpdate(ChannelBase):
    channel_id: str


class ChannelInDBBase(ChannelBase):
    channel_id: str
    created_at: datetime
    last_updated_at: datetime

    class Config:
        orm_mode = True

class Channel(ChannelInDBBase):
    pass

class ChannelInDB(ChannelInDBBase):
    pass