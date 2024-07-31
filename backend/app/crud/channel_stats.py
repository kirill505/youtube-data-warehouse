from sqlalchemy.orm import Session
from app.models.channel_stats import ChannelStats
from app.schemas.channel_stats import ChannelStatsCreate
from datetime import datetime

def create_channel_stats(db: Session, stats: ChannelStatsCreate):
    db_stats = ChannelStats(
        channel_id=stats.channel_id,
        subscriber_count=stats.subscriber_count,
        video_count=stats.video_count,
        view_count=stats.view_count,
        last_updated_at=datetime.utcnow()
    )
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)
    return db_stats
