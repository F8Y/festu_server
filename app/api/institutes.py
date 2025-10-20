from fastapi import APIRouter, HTTPException, Path
from app.models.institute import (
    InstituteListResponse,
    InstituteResponse,
    GroupListResponse,
    GroupResponse
)
from app.services.institute_service import get_institute_service

router = APIRouter()


@router.get(
    "",
    response_model=InstituteListResponse,
    summary="Получить список всех институтов",
    description="Возвращает список всех институтов университета с их ID и названиями"
)
async def get_institutes():
    """
    Получить список всех институтов

    Returns:
        InstituteListResponse: Список институтов с их ID и названиями
    """
    service = get_institute_service()
    institutes = service.get_all_institutes()

    return InstituteListResponse(
        institutes=[InstituteResponse(**inst) for inst in institutes],
        total=len(institutes)
    )


@router.get(
    "/{institute_id}/groups",
    response_model=GroupListResponse,
    summary="Получить группы института",
    description="Возвращает список всех групп указанного института"
)
async def get_institute_groups(
        institute_id: str = Path(
            ...,
            description="ID института (например, 'ims', 'itps')",
            example="ims"
        )
):
    """
    Получить список групп конкретного института

    Args:
        institute_id: ID института

    Returns:
        GroupListResponse: Список групп института

    Raises:
        HTTPException 404: Если институт не найден
    """
    service = get_institute_service()

    # Получаем группы (выбросит 404 если института нет)
    groups = service.get_institute_groups(institute_id)

    # Получаем название института
    all_institutes = service.get_all_institutes()
    institute_name = next(
        (inst["name"] for inst in all_institutes if inst["id"] == institute_id),
        institute_id
    )

    return GroupListResponse(
        institute_id=institute_id,
        institute_name=institute_name,
        groups=[GroupResponse(**group) for group in groups],
        total=len(groups)
    )