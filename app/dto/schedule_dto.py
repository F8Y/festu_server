from pydantic import BaseModel, validator
from datetime import datetime

class ScheduleDTO(BaseModel):
    Time: str
    GroupID: int
    HTML: str

    @validator("Time")
    def validate_time_format(cls, v):
        try:
            datetime.strptime(v, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Time must be in format dd.mm.yyyy")
        return v
