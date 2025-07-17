from fastapi import APIRouter, Header, HTTPException
from app.core.config import RATE_LIMIT
from app.services.validator import validate_headers, send_request_to_festu
from app.services.week_parser import get_week_range
from app.services.html_parser import extract_week_schedule
from app.services.json_parser import parse_schedule_to_json
from app.core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/")
@limiter.limit(RATE_LIMIT)
async def validate_and_fetch(
        request: Request,
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
