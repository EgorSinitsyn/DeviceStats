from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

# from app import models, schemas

import models, schemas

def create_stats(db: Session, device_id: int, stats: schemas.StatsCreate):
    """
    Функция по сохранению записи в формате (x, y, z) для устройства device_id
    :param db:
    :param device_id:
    :param stats:
    :return:
    """
    # Проверяем, есть ли устройство. Если нет – создаём для удобства
    device = db.query(models.Device).filter(models.Device.id == device_id).first()
    if not device:
        device = models.Device(id=device_id)
        db.add(device)
        db.commit()
        db.refresh(device)

    # Создаем новую запись статистики для устройства. Значения x, y и z берутся из объекта stats (типа StatsCreate), который был передан в качестве тела запроса.
    db_stats = models.DeviceStats(
        device_id=device_id,
        x=stats.x,
        y=stats.y,
        z=stats.z
    )
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)

    # Возвращаем созданную запись статистики, используя схему StatsOut
    return db_stats


def get_aggregated_stats(
    db: Session,
    device_id: int,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
):
    """
    Функция вычисляет агрегированные статистические показатели для записей,
    связанных с заданным устройством (device_id). Агрегируется сумма значений x, y и z.
    Если заданы временные рамки (start_time и end_time), производится фильтрация по полю created_at.
    :param db:
    :param device_id: ID устройства
    :param start_time: Начало временного интервала (опционально)
    :param end_time: Конец временного интервала (опционально)
    """

    # Формируем запрос для выборки записей статистики для указанного устройства.
    query = db.query(models.DeviceStats).filter(models.DeviceStats.device_id == device_id)

    # Если передан параметр start_time, выбираем записи, созданные после указанного времени.
    if start_time:
        query = query.filter(models.DeviceStats.created_at >= start_time)
    # Если передан параметр end_time, выбираем записи, созданные до указанного времени.
    if end_time:
        query = query.filter(models.DeviceStats.created_at <= end_time)

    # Получаем все записи, удовлетворяющие условиям.
    data = query.all()
    if not data:
        return None

    # Вычисляем агрегированные значения:
    # Для каждой записи считаем сумму (x+y+z)
    values = [row.x + row.y + row.z for row in data]
    # Сортируем значения для вычисления медианы
    sorted_values = sorted(values)
    count = len(sorted_values)
    summation = sum(sorted_values)
    min_value = min(sorted_values)
    max_value = max(sorted_values)

    # Вычисляем медиану:
    # Если количество записей нечетное, медиана – это центральное значение.
    # Если четное – медиана вычисляется как среднее двух центральных значений.
    if count % 2 == 1:
        median_value = sorted_values[count // 2]
    else:
        mid = count // 2
        median_value = (sorted_values[mid - 1] + sorted_values[mid]) / 2

    # Возвращаем агрегированные результаты в виде объекта, который соответствует схеме AnalysisResult.
    return schemas.AnalysisResult(
        device_id=device_id,
        min_value=min_value,
        max_value=max_value,
        count=count,
        summation=summation,
        median=median_value
    )