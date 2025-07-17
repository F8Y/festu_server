from fastapi import HTTPException
from app.models.headers import HeaderData
from app.providers.festu_adapter import fetch_schedule_from_festu

def validate_headers(Time: str, GroupID: int) -> HeaderData:
    try:
        return HeaderData(Time=Time, GroupID=GroupID)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def send_request_to_festu(headers: HeaderData) -> str:
    return await fetch_schedule_from_festu(headers.Time, headers.GroupID)
