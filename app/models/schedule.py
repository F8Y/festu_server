from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
from datetime import datetime


class TeacherInfo(BaseModel):
    """Информация о преподавателе"""
    model_config = ConfigDict(extra='allow')

    name: str = Field(..., description="ФИО преподавателя")
    email: Optional[str] = Field(None, description="Email преподавателя")


class PairInfo(BaseModel):
    """Информация о паре"""
    model_config = ConfigDict(extra='allow')

    number: Optional[int] = Field(None, description="Номер пары (1-6)")
    time: Optional[str] = Field(None, description="Время пары (например, '8:05-9:35')")
    subject: str = Field(..., description="Название предмета")
    auditorium: str = Field(..., description="Номер аудитории")
    group: str = Field(..., description="Номер группы")
    teacher: TeacherInfo = Field(..., description="Информация о преподавателе")
    comment: Optional[str] = Field(None, description="Комментарий (например, тип пары)")


class DaySchedule(BaseModel):
    """Расписание на один день"""
    model_config = ConfigDict(extra='allow')

    date: str = Field(..., description="Дата в формате dd.mm.yyyy")
    day: str = Field(..., description="Название дня недели")
    pairs: List[PairInfo] = Field(..., description="Список пар в этот день")


class ScheduleResponse(BaseModel):
    """Полное расписание на неделю"""
    model_config = ConfigDict(extra='allow')

    week: str = Field(..., description="Диапазон недели (например, '14.10.2025–20.10.2025')")
    days: List[DaySchedule] = Field(..., description="Расписание по дням")


class ScheduleRequest(BaseModel):
    """Параметры запроса расписания"""
    group_id: int = Field(..., gt=0, description="ID группы")
    time: str = Field(..., description="Дата в формате dd.mm.yyyy")

    @field_validator("time")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        """Валидация формата даты"""
        try:
            datetime.strptime(v, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Time must be in format dd.mm.yyyy")
        return v