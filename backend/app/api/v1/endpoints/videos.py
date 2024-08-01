from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Any, List
from googleapiclient.discovery import build
from datetime import datetime
from app import crud
from app.schemas.video import Video, VideoCreate, VideoUpdate
from app.utils.dependencies import get_db
from app.core.config import settings
from app.youtube.client import YouTubeClient


router = APIRouter()


@router.post("/", response_model=Video)
def create_video(
        video_url: str,
        db: Session = Depends(get_db)
) -> Any:
    video_id = video_url.split("v=")[-1]

    try:
        video = crud.video.create_new_video(db=db, video_id=video_id)
    except ValueError as e:
        print("KeyError:", e)
        raise HTTPException(status_code=404, detail=str(e))

    return video


@router.put("/{video_id}", response_model=Video)
def update_video(
        video_id: str,
        db: Session = Depends(get_db)
) -> Any:
    try:
        video = crud.video.update_video(db=db, video_id=video_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return video


@router.get("/top50", response_model=List[VideoCreate])
async def get_top_50_videos(
        db: Session = Depends(get_db)
) -> Any:
    try:
        top_videos = crud.video.get_top_videos(db=db, limit=10)
    except Exception as e:
        print("KeyError:", e)
        raise HTTPException(status_code=500, detail="Ошибка при получении топ-50 видео")

    return top_videos
