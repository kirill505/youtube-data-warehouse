from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import Any, List
from app import crud
from app.schemas.video import Video, VideoCreate, VideoUpdate
from app.db.session import get_db


router = APIRouter()


@router.post("/", response_model=Video)
async def create_video(
        video_url: str,
        db: AsyncSession = Depends(get_db)
) -> Any:
    video_id = video_url.split("v=")[-1]

    try:
        video = await crud.video.create_new_video(db=db, video_id=video_id)
    except ValueError as e:
        print("KeyError:", e)
        raise HTTPException(status_code=404, detail=str(e))

    return video


@router.put("/{video_id}", response_model=Video)
async def update_video(
        video_id: str,
        db: AsyncSession = Depends(get_db)
) -> Any:
    try:
        video = await crud.video.update_video(db=db, video_id=video_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return video


@router.get("/top_videos", response_model=List[VideoCreate])
async def get_top_videos(
        regioncode: str,
        limit: int = 200
) -> Any:
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")

    try:
        top_videos = await crud.video.get_top_videos(regioncode, limit=limit)
    except Exception as e:
        print("KeyError:", e)
        raise HTTPException(status_code=500, detail="Error fetching top videos")

    return top_videos


@router.get("/search", response_model=List[VideoCreate])
async def search_videos(
        query: str,
        limit: int = 200,
        db: AsyncSession = Depends(get_db)
) -> Any:
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit must be greater than 0")

    try:
        found_videos = await crud.video.search_and_store_videos(db, query, limit)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error searching videos")

    return found_videos
