from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import video_stats as crud_video_stats
from app.schemas import video_stats as schemas_video_stats
from app.utils.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas_video_stats.VideoStats)
def create_video_stats(
    video_stats: schemas_video_stats.VideoStatsCreate, db: Session = Depends(get_db)
):
    db_video_stats = crud_video_stats.create_video_stats(db=db, stats=video_stats)
    if db_video_stats is None:
        raise HTTPException(status_code=400, detail="Error creating video stats")
    return db_video_stats
