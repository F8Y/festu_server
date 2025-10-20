from pydantic import BaseModel, Field
from typing import List


class InstituteResponse(BaseModel):
    id: str = Field(..., description="ID института")
    name: str = Field(..., description="Полное название института")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "ims",
                "name": "Институт международного сотрудничества"
            }
        }


class InstituteListResponse(BaseModel):
    institutes: List[InstituteResponse]
    total: int = Field(..., description="Общее количество институтов")

    class Config:
        json_schema_extra = {
            "example": {
                "institutes": [
                    {"id": "ims", "name": "Институт международного сотрудничества"},
                    {"id": "itps", "name": "Институт транспортного строительства"}
                ],
                "total": 2
            }
        }


class GroupResponse(BaseModel):
    key: str = Field(..., description="ID группы (используется для запроса расписания)")
    name: str = Field(..., description="Полное название группы")

    class Config:
        json_schema_extra = {
            "example": {
                "key": "370",
                "name": "И41 - Менеджмент (Международный менеджмент)"
            }
        }


class GroupListResponse(BaseModel):
    institute_id: str = Field(..., description="ID института")
    institute_name: str = Field(..., description="Название института")
    groups: List[GroupResponse]
    total: int = Field(..., description="Количество групп в институте")

    class Config:
        json_schema_extra = {
            "example": {
                "institute_id": "ims",
                "institute_name": "Институт международного сотрудничества",
                "groups": [
                    {"key": "370", "name": "И41 - Менеджмент"}
                ],
                "total": 1
            }
        }
