from fastapi import HTTPException
from app.dto.schedule_dto import ScheduleDTO
from app.dto.schedule_raw_dto import ScheduleRawHTMLDTO
from app.services.html_parser import extract_week_schedule
from app.services.week_parser import get_week_range
from app.services.json_parser import parse_schedule_to_json

async def forward_schedule_to(dto: ScheduleDTO):
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

    return structured_json
