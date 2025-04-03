# from app.celery_app import celery_app
# from app.database import SessionLocal
# from app import crud, models

from celery_app import celery_app
from database import SessionLocal
import crud, models

@celery_app.task
def recalculate_stats_for_all_devices():
    """
    Пример задачи: пересчитать агрегированные показатели для всех устройств.
    Можно, например, пройтись по всем устройствам и сохранить результаты анализа в кэш или отдельную таблицу.
    """
    db = SessionLocal()
    try:
        # Получаем список всех устройств
        devices = db.query(models.Device).all()
        for device in devices:
            result = crud.get_aggregated_stats(db, device.id)
            # Здесь можно, например, сохранить результат в кэш или просто вывести в лог
            print(f"Aggregated stats for device {device.id}: {result}")
    finally:
        db.close()