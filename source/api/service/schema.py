from datetime import datetime
from pydantic import BaseModel, field_validator



class XRayStatusResponse(BaseModel):
    execution_result_code: int
    details: str


class DateQuery(BaseModel):
    start_date: datetime

    @field_validator("start_date")
    def validate_start_date(cls, value):
        # Define your desired datetime format
        datetime_format = "%d-%m-%Y"
        try:
            return datetime.strptime(value, datetime_format)
        except ValueError:
            raise ValueError(f"Invalid datetime format. Expected format: {datetime_format}")