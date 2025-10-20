import httpx
from fastapi import HTTPException
from app.core.config import FESTU_ENDPOINT

async def fetch_schedule_from_festu(time: str, group_id: int) -> str:
    payload = {
        "Time": time,
        "GroupID": group_id
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(FESTU_ENDPOINT, data=payload)

        if response.status_code != 200:
            raise HTTPException(status_code=502, detail="FESTU gives error")

        return response.text

    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail="Festu is not available")