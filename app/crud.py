from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import models, schemas

def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(**video.dict())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_video(db: Session, video_id: int):
    return db.query(models.Video).filter(models.Video.id == video_id).first()

def get_videos(
    db: Session,
    status: Optional[List[str]] = None,
    camera_number: Optional[List[int]] = None,
    location: Optional[List[str]] = None,
    start_time_from: Optional[datetime] = None,
    start_time_to: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(models.Video)
    
    if status:
        query = query.filter(models.Video.status.in_(status))
    if camera_number:
        query = query.filter(models.Video.camera_number.in_(camera_number))
    if location:
        query = query.filter(models.Video.location.in_(location))
    if start_time_from:
        query = query.filter(models.Video.start_time >= start_time_from)
    if start_time_to:
        query = query.filter(models.Video.start_time <= start_time_to)
    
    return query.offset(skip).limit(limit).all()

def update_video_status(db: Session, video_id: int, status: str):
    db_video = get_video(db, video_id)
    if db_video:
        db_video.status = status
        db.commit()
        db.refresh(db_video)
    return db_video