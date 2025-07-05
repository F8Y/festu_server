from app.dto.schedule_raw_dto import ScheduleRawHTMLDTO
from app.services.week_parser import extract_week_schedule, get_week_range
from app.services.json_parser import parse_schedule_to_json

async def parse_html(dto: ScheduleRawHTMLDTO) -> dict | None:
    """
    Получает DTO с Time и HTML, возвращает JSON-структуру расписания.
    """
    filtered_html = extract_week_schedule(dto.HTML, dto.Time)

    if not filtered_html:
        return None

    monday, sunday = get_week_range(dto.Time)
    return parse_schedule_to_json(filtered_html, monday, sunday)
