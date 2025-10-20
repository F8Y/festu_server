from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class TeacherInfo(BaseModel):
    name: str = Field(..., description="ФИО преподавателя")
    email: Optional[str] = Field(None, description="Email преподавателя")


class PairInfo(BaseModel):
    number: Optional[int] = Field(None, description="Номер пары(1 - 6)")
    time: Optional[str] = Field(None, description="Время пары (начало - конец)")
    subject: str = Field(..., description="Название предмета")
    auditorium: str = Field(..., description="Номер аудитории")
    group: str = Field(..., description="Номер группы")
    teacher: TeacherInfo = Field(..., description="Информация о преподавателе")
    comment: Optional[str] = Field(None, description="Комментарий")


class DaySchedule(BaseModel):
    Time: str = Field(..., description="Дата в формате dd.mm.yyyy")
    day: str = Field(..., description="Название дня недели")
    pairs: List[PairInfo] = Field(..., description="Список пар на день")


class ScheduleResponse(BaseModel):
    week: str = Field(..., description="Диапазон недели (начало - конец)")
    days: List[DaySchedule] = Field(..., description="Расписание по дням")

    class Config:
        json_schema_extra = {
            "example": {
                "week": "14.10.2025-20.10.2025",
                "days": [
                    {
                        "Time": "14.10.2025",
                        "day": "Понедельник",
                        "pairs": [
                            {
                                "number": 1,
                                "time": "8:05-9:35",
                                "subject": "Анализ",
                                "auditorium": "202",
                                "group": "И41",
                                "teacher": {
                                    "name": "Гладкий Д.В.",
                                    "email": "gldv@mail.ru"
                                },
                                "comment": "Лекция"
                            }
                        ]
                    }
                ]
            }
        }


class ScheduleRequest(BaseModel):
    group_id: int = Field(..., gt=0, description="ID группы")
    Time: str = Field(..., description="Дата в формате dd.mm.yyyy")

    @field_validator("Time")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Date must be in format dd.mm.yyyy")
        return v
