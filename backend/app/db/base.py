from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Initialize all models to avoid circular import issues
def initialize_models():
    from app.models import Channel, Video, ChannelStats, VideoStats
    Channel()
    Video()
    ChannelStats()
    VideoStats()
