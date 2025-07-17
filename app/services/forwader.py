from fastapi import HTTPException
from app.dto.schedule_dto import ScheduleDTO
from app.dto.schedule_raw_dto import ScheduleRawHTMLDTO
from app.services.html_parser import extract_week_schedule
from app.services.week_parser import get_week_range
from app.services.json_parser import parse_schedule_to_json
from app.core.cache import schedule_cache as cache

def make_cache_key(dto:ScheduleDTO) -> str:
    return f"{dto.Time}_{dto.GroupID}"

async def forward_schedule_to(dto: ScheduleDTO):
    key = make_cache_key(dto)

    if key in cache:
        return cache[key]

    raw_dto = ScheduleRawHTMLDTO(Time=dto.Time, HTML=dto.HTML)
    filtered_html = extract_week_schedule(raw_dto.HTML, raw_dto.Time)

    if not filtered_html:
        raise HTTPException(
            status_code=200,
            detail={
                "status": "no_schedule",
                "message": "Нет пар на этой неделе"
            }
        )

    monday, sunday = get_week_range(raw_dto.Time)
    structured_json = parse_schedule_to_json(filtered_html, monday, sunday)


    cache[key] = structured_json
    return structured_json
