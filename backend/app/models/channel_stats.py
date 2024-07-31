from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from app.db.base import Base


class ChannelStats(Base):
    __tablename__ = "channel_stats"

    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, ForeignKey("channels.channel_id"), nullable=False)
    subscriber_count = Column(Integer)
    video_count = Column(Integer)
    view_count = Column(BigInteger)
    last_updated_at = Column(DateTime)
