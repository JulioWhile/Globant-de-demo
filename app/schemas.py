from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class Department(BaseModel):
    id: int
    department: str

class Job(BaseModel):
    id: int
    job: str

class HiredEmployeeBase(BaseModel):
    name: str = Field(..., max_length=100)
    department_id: int
    job_id: int

class HiredEmployeeCreate(HiredEmployeeBase):
    datetime: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("datetime")
    def datetime_must_be_in_the_past(self, value):
        if value > datetime.utcnow():
            raise ValueError("Datetime cannot be in the future")
        return value

class HiredEmployee(HiredEmployeeBase):
    id: int
    datetime: datetime

    class Config:
        orm_mode = True