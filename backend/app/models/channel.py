from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Channel(Base):
    __tablename__ = 'channels'

    channel_id = Column(String, primary_key=True, index=True)
    channel_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    videos = relationship("Video", back_populates="channel", lazy="joined")
