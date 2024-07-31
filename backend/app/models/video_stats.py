from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from app.db.base import Base


class VideoStats(Base):
    __tablename__ = "video_stats"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, ForeignKey("videos.video_id"), nullable=False)
    view_count = Column(BigInteger)
    like_count = Column(Integer)
    comment_count = Column(Integer)
    last_updated_at = Column(DateTime)
