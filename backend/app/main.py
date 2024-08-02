from fastapi import FastAPI
from app.api.v1.endpoints import channels, videos, channel_stats, video_stats
from app.db.session import engine
from app.db.base import Base

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(channels.router, prefix="/api/v1/channels", tags=["channels"])
app.include_router(videos.router, prefix="/api/v1/videos", tags=["videos"])
app.include_router(channel_stats.router, prefix="/api/v1/channel_stats", tags=["channel_stats"])
app.include_router(video_stats.router, prefix="/api/v1/video_stats", tags=["video_stats"])
