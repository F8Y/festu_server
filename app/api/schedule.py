from fastapi import APIRouter, Query, Request
from app.models.schedule import ScheduleResponse
from app.services.forwarder import get_schedule
from app.core.limiter import limiter
from app.core.config import RATE_LIMIT

router = APIRouter()


@router.get(
    "",
    response_model=ScheduleResponse,
    response_model_exclude_none=True,  # Исключаем None значения из ответа
    summary="Получить расписание группы",
    description="Возвращает расписание на неделю для указанной группы. Результат кэшируется на 10 минут."
)
@limiter.limit(RATE_LIMIT)
async def get_group_schedule(
        request: Request,
        group_id: int = Query(
            ...,
            gt=0,
            alias="group_id",
            description="ID группы (из списка групп института)",
            example=370
        ),
        time: str = Query(
            ...,
            alias="time",
            description="Дата в формате dd.mm.yyyy (любой день нужной недели)",
            example="25.10.2025",
            pattern=r"^\d{2}\.\d{2}\.\d{4}$"
        )
):
    """
    Получить расписание группы на неделю

    Система автоматически определяет неделю по указанной дате и возвращает
    полное расписание с понедельника по воскресенье.

    Args:
        group_id: ID группы (можно получить через /api/v1/institutes/{id}/groups)
        time: Любой день недели в формате dd.mm.yyyy

    Returns:
        ScheduleResponse: Расписание на всю неделю

    Raises:
        HTTPException 400: Неверный формат даты
        HTTPException 404: Группа не найдена или нет расписания на эту неделю
        HTTPException 429: Превышен лимит запросов
        HTTPException 502/503: Проблемы с внешним API
    """
    schedule = await get_schedule(group_id, time)
    return schedule