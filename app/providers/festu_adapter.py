import httpx
from fastapi import HTTPException
from app.core.config import FESTU_ENDPOINT
import logging

logger = logging.getLogger(__name__)


async def fetch_schedule_from_festu(time: str, group_id: int) -> str:
    payload = {
        "Time": time,
        "GroupID": group_id
    }

    logger.info(f"Fetching from FESTU: {FESTU_ENDPOINT}")
    logger.info(f"Payload: Time={time}, GroupID={group_id}")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:  # Увеличен timeout
            response = await client.post(FESTU_ENDPOINT, data=payload)

        logger.info(f"FESTU response status: {response.status_code}")
        logger.debug(f"FESTU response headers: {response.headers}")

        if response.status_code != 200:
            logger.error(f"FESTU returned status {response.status_code}")
            raise HTTPException(
                status_code=502,
                detail=f"FESTU API error: status {response.status_code}"
            )

        return response.text

    except httpx.TimeoutException as e:
        logger.error(f"Timeout connecting to FESTU: {e}")
        raise HTTPException(
            status_code=504,
            detail="FESTU API timeout"
        )
    except httpx.RequestError as e:
        logger.error(f"Request error to FESTU: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"FESTU is not available: {str(e)}"
        )