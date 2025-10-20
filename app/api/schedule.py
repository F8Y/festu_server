from fastapi import APIRouter, Query, Request
from app.models.schedule import ScheduleResponse
from app.services.forwarder import get_schedule
from app.core.limiter import limiter
from app.core.config import RATE_LIMIT

router = APIRouter()

@router.get(
    "/",
    response_model=ScheduleResponse,
    summary="Получить расписание группы",
    description="Возвращает расписание на неделю для указанной группы. Кэшируется на 10 минут"
)
@limiter.limit(RATE_LIMIT)
async def get_group_schedule(
        request: Request,
        group_id: int = Query(
            ...,
            gt=0,
            description="ID группы из списка групп института",
            example=370
        ),
        Time: str = Query(
            ...,
            description="Дата в формате dd.mm.yyyy (любой день необходимой недели)",
            example="20.10.2025",
            pattern=r"^\d{2}\.\d{2}\.\d{4}$"
        )
):
    schedule = await get_schedule(group_id, Time)
    return schedule