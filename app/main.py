from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

# from app.tasks import recalculate_stats_for_all_devices
# from app.database import get_db, Base, engine
# from . import crud, schemas

from tasks import recalculate_stats_for_all_devices
from database import get_db, Base, engine
import crud, schemas

app = FastAPI(
    title="Devise_stat_service",
    description="Сервис_для_сбора_и_анализа_данных_с_устройств",
    version="1.0.0",
)

# Инициализация таблицы
Base.metadata.create_all(bind=engine)

@app.post("/devices/{device_id}/data", response_model=schemas.StatsOut)
def create_device_stats(
        device_id: int,
        stats_in: schemas.StatsCreate,
        db: Session = Depends(get_db)
):
    """
    Функция по сохранению записи в формате (x, y, z) для устройства device_id
    :param device_id:
    :param stats_in:
    :param db:
    :return:
    """
    device_stats = crud.create_stats(db=db, device_id=device_id, stats=stats_in)
    return device_stats


@app.get("/devices/{device_id}/data", response_model=schemas.AnalysisResult)
def get_stats_for_device(
        device_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        db: Session = Depends(get_db)
):
    """
    Функция по получению агрегированных данных (min, max, count, sum, median) для устройства device_id за период [start_time, end_time] (если переданы) или за всё время.
    :param device_id:
    :param start_date:
    :param end_date:
    :param db:
    :return:
    """
    analysis_result = crud.get_aggregated_stats(
        db,
        device_id=device_id,
        start_time=start_date,
        end_time=end_date
    )
    if not analysis_result:
        raise HTTPException(status_code=404, detail="No data found for this device")
    return analysis_result


@app.get("/devices/{device_id}/data/all", response_model=schemas.AnalysisResult)
def get_stats_for_device_all_time(
        device_id: int,
        db: Session = Depends(get_db)
):
    """
    Функция по получению агрегированных данных (min, max, count, sum, median) для устройства device_id за всё время.
    :param device_id:
    :param db:
    :return:
    """
    analysis_result = crud.get_aggregated_stats(
        db,
        device_id=device_id
    )
    if not analysis_result:
        raise HTTPException(status_code=404, detail="No data found for this device")
    return analysis_result


# Пример задачи, которая будет запускаться по расписанию
@app.post("/tasks/recalculate")
def trigger_recalculate():
    task = recalculate_stats_for_all_devices.delay()
    return {"task_id": task.id, "status": "Task started"}