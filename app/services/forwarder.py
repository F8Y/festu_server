from fastapi import HTTPException
from app.services.week_parser import extract_week_schedule, get_week_range
from app.services.json_parser import parse_schedule_to_json
from app.core.cache import schedule_cache as cache
from app.providers.festu_adapter import fetch_schedule_from_festu
from app.services.institute_service import get_institute_service


def make_cache_key(group_id: int, Time: str) -> str:
    """Создать ключ для кэша"""
    return f"{group_id}_{Time}"


async def get_schedule(group_id: int, Time: str) -> dict:
    """Получить расписание для группы на указанную дату"""
    # Валидация существования группы
    service = get_institute_service()
    if not service.validate_group_id(group_id):
        raise HTTPException(
            status_code=404,
            detail=f"Group with ID {group_id} not found"
        )

    # Проверяем кэш
    cache_key = make_cache_key(group_id, Time)

    if cache_key in cache:
        return cache[cache_key]

    # Запрос к внешнему API
    html = await fetch_schedule_from_festu(Time, group_id)

    # Извлекаем расписание на неделю
    filtered_html = extract_week_schedule(html, Time)

    if not filtered_html:
        raise HTTPException(
            status_code=404,
            detail="No schedule found for this week"
        )

    # Парсим в JSON
    monday, sunday = get_week_range(Time)
    structured_json = parse_schedule_to_json(filtered_html, monday, sunday)

    # Сохраняем в кэш
    cache[cache_key] = structured_json

    return structured_json
