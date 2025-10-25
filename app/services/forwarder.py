from fastapi import HTTPException
from app.services.week_parser import get_week_range, extract_week_schedule
from app.services.json_parser import parse_schedule_to_json
from app.core.cache import schedule_cache as cache
from app.providers.festu_adapter import fetch_schedule_from_festu
from app.services.institute_service import get_institute_service


def make_cache_key(group_id: int, time: str) -> str:
    """
    Создать ключ для кэша

    Args:
        group_id: ID группы
        time: Дата в формате dd.mm.yyyy

    Returns:
        Ключ кэша в формате "groupid_time"
    """
    return f"{group_id}_{time}"


async def get_schedule(group_id: int, time: str) -> dict:
    """
    Получить расписание для группы на указанную дату

    Использует кэш для оптимизации запросов к внешнему API.
    Валидирует существование группы перед запросом.

    Args:
        group_id: ID группы
        time: Дата в формате dd.mm.yyyy

    Returns:
        Структурированное расписание в формате JSON

    Raises:
        HTTPException 404: Если группа не существует или нет расписания
        HTTPException 502/503: Если проблемы с внешним API
    """
    # Валидация существования группы
    service = get_institute_service()
    if not service.validate_group_id(group_id):
        raise HTTPException(
            status_code=404,
            detail=f"Group with ID {group_id} not found"
        )

    # Проверяем кэш
    cache_key = make_cache_key(group_id, time)

    if cache_key in cache:
        return cache[cache_key]

    # Запрос к внешнему API (используем time, как требует FESTU)
    html = await fetch_schedule_from_festu(time, group_id)

    # Извлекаем расписание на неделю
    filtered_html = extract_week_schedule(html, time)

    if not filtered_html:
        raise HTTPException(
            status_code=404,
            detail="No schedule found for this week"
        )

    # Парсим в JSON
    monday, sunday = get_week_range(time)
    structured_json = parse_schedule_to_json(filtered_html, monday, sunday)

    # Сохраняем в кэш
    cache[cache_key] = structured_json

    return structured_json