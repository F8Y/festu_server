from fastapi import HTTPException
from app.models.headers import HeaderData
from app.core.config import FESTU_ENDPOINT
import httpx

def validate_headers(Time: str, GroupID: int) -> HeaderData:
    try:
        return HeaderData(Time=Time, GroupID=GroupID)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def send_request_to_festu(headers: HeaderData) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            FESTU_ENDPOINT,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"Time": headers.Time, "GroupID": headers.GroupID}
        )

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Festu service error")

    return response.text
