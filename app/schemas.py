from typing import Optional

from pydantic import BaseModel, Field, field_validator
from datetime import datetime as _datetime, timezone


class Department(BaseModel):
    id: int
    department: str

    class Config:
        from_attributes = True

class Job(BaseModel):
    id: int
    job: str

    class Config:
        from_attributes = True

class DepartmentCreate(BaseModel):
    department: str = Field(..., max_length=100)


class JobCreate(BaseModel):
    job: str = Field(..., max_length=100)


class HiredEmployeeBase(BaseModel):
    name: str = Field(..., max_length=100)
    department_id: int
    job_id: Optional[int]


class HiredEmployeeCreate(HiredEmployeeBase):
    id: int
    name: str
    datetime: _datetime
    department_id: int
    job_id: Optional[int]

    @field_validator("datetime")
    def hired_datetime_must_be_in_the_past(cls, value):
        if value > _datetime.now(timezone.utc):
            raise ValueError("Hired datetime cannot be in the future")
        return value


class HiredEmployee(HiredEmployeeBase):
    id: int
    datetime: _datetime

    class Config:
        from_attributes = True
