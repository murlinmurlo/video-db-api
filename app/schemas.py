from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta
from typing import List, Optional

class VideoBase(BaseModel):
    video_path: str = Field(..., min_length=1, description="Путь до видеофайла")
    start_time: datetime = Field(..., description="Время начала записи")
    duration: timedelta = Field(..., description="Длительность видео")
    camera_number: int = Field(..., gt=0, description="Номер камеры")
    location: str = Field(..., min_length=1, description="Локация камеры")

    @validator('duration')
    def duration_positive(cls, v):
        if v.total_seconds() <= 0:
            raise ValueError('duration must be positive')
        return v

class VideoCreate(VideoBase):
    pass

class VideoUpdateStatus(BaseModel):
    status: str = Field(..., description="Статус видео")

    @validator('status')
    def status_valid(cls, v):
        allowed_statuses = ["new", "transcoded", "recognized"]
        if v not in allowed_statuses:
            raise ValueError(f'status must be one of {allowed_statuses}')
        return v

class VideoResponse(VideoBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class VideoFilter(BaseModel):
    status: Optional[List[str]] = None
    camera_number: Optional[List[int]] = None
    location: Optional[List[str]] = None
    start_time_from: Optional[datetime] = None
    start_time_to: Optional[datetime] = None