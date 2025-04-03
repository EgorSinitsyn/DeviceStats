from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StatsCreate(BaseModel):
    x: float
    y: float
    z: float

class StatsOut(BaseModel):
    id: int
    device_id: int
    x: float
    y: float
    z: float
    created_at: datetime

    class Config:
        orm_mode = True

class AnalysisResult(BaseModel):
    device_id: int
    min_value: float
    max_value: float
    count: int
    summation: float
    median: float