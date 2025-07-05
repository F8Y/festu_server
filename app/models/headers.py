from pydantic import BaseModel, validator
from datetime import datetime

class HeaderData(BaseModel):
    Time: str
    GroupID: int

    @validator("Time")
    def validate_time_format(cls, v):
        try:
            datetime.strptime(v, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Time must be 'dd.mm.yyyy'")
        return v
