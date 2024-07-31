from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Video(Base):
    __tablename__ = 'videos'

    video_id = Column(String, primary_key=True, index=True)
    channel_id = Column(String, ForeignKey('channels.channel_id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=False)
    last_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    channel = relationship("Channel", back_populates="videos", lazy="joined")
