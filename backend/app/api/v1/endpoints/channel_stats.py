from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import channel_stats as crud_channel_stats
from app.schemas import channel_stats as schemas_channel_stats
from app.utils.dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas_channel_stats.ChannelStats)
def create_channel_stats(
    channel_stats: schemas_channel_stats.ChannelStatsCreate, db: Session = Depends(get_db)
):
    print(channel_stats)
    db_channel_stats = crud_channel_stats.create_channel_stats(db=db, stats=channel_stats)
    if db_channel_stats is None:
        raise HTTPException(status_code=400, detail="Error creating channel stats")
    return db_channel_stats
