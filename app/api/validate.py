from fastapi import APIRouter, Header, HTTPException
from app.services.validator import validate_headers, send_request_to_festu
from app.services.week_parser import get_week_range
from app.services.html_parser import extract_week_schedule
from app.services.json_parser import parse_schedule_to_json

router = APIRouter()

@router.post("/")
async def validate_and_fetch(
        Time: str = Header(...),
        GroupID: int = Header(...)
):
    headers = validate_headers(Time, GroupID)

    html = await send_request_to_festu(headers)

    filtered_html = extract_week_schedule(html, headers.Time)
    if not filtered_html:
        raise HTTPException(
            status_code=200,
            detail={
                "status": "no_schedule",
                "message": "Нет пар на этой неделе"
            }
        )

    monday, sunday = get_week_range(headers.Time)
    structured_json = parse_schedule_to_json(filtered_html, monday, sunday)

    return structured_json
