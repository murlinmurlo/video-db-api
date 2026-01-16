from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from . import crud, schemas
from .database import get_db

router = APIRouter()

@router.post("/videos", response_model=schemas.VideoResponse, status_code=201)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    """
    Добавить новое видео в БД
    """
    return crud.create_video(db=db, video=video)

@router.get("/videos", response_model=List[schemas.VideoResponse])
def read_videos(
    status: Optional[List[str]] = Query(None, description="Фильтр по статусам"),
    camera_number: Optional[List[int]] = Query(None, description="Фильтр по номерам камер"),
    location: Optional[List[str]] = Query(None, description="Фильтр по локациям"),
    start_time_from: Optional[datetime] = Query(None, description="Видео после указанного времени"),
    start_time_to: Optional[datetime] = Query(None, description="Видео до указанного времени"),
    db: Session = Depends(get_db)
):
    """
    Получить список всех видео с поддержкой фильтров
    """
    videos = crud.get_videos(
        db=db,
        status=status,
        camera_number=camera_number,
        location=location,
        start_time_from=start_time_from,
        start_time_to=start_time_to
    )
    return videos

@router.get("/videos/{video_id}", response_model=schemas.VideoResponse)
def read_video(video_id: int, db: Session = Depends(get_db)):
    """
    Получить информацию о видео по ID
    """
    db_video = crud.get_video(db=db, video_id=video_id)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video

@router.patch("/videos/{video_id}/status", response_model=schemas.VideoResponse)
def update_video_status(
    video_id: int,
    status_update: schemas.VideoUpdateStatus,
    db: Session = Depends(get_db)
):
    """
    Обновить статус видео
    """
    db_video = crud.update_video_status(db=db, video_id=video_id, status=status_update.status)
    if db_video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_video