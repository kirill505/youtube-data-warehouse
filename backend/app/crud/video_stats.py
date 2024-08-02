from sqlalchemy.orm import Session
from app.models.video_stats import VideoStats
from app.schemas.video_stats import VideoStatsCreate
from datetime import datetime, timezone

def create_video_stats(db: Session, stats: VideoStatsCreate):
    db_stats = VideoStats(
        video_id=stats.video_id,
        view_count=stats.view_count,
        like_count=stats.like_count,
        comment_count=stats.comment_count,
        last_updated_at=datetime.now(timezone.utc)
    )
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)
    return db_stats
