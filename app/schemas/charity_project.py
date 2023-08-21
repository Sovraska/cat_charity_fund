from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator

from app.core.config import settings


class CharityProjectBase(BaseModel):
    name: str
    description: str
    full_amount: int


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=settings.min_length_string,
        max_length=settings.max_length_string,
    )
    description: str = Field(..., min_length=settings.min_length_string)

    @validator("full_amount")
    def check_full_amount(cls, value):
        if value <= settings.full_amount_minimum:
            raise ValueError("full_amount не может быть ниже 0")
        return value


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=settings.min_length_string,
        max_length=settings.max_length_string,
    )
    description: Optional[str] = Field(None, min_length=settings.min_length_string)
    full_amount: Optional[int]

    @validator("full_amount")
    def check_full_amount(cls, value):
        if value <= settings.full_amount_minimum:
            raise ValueError("full_amount не может быть ниже 0")
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime = None

    class Config:
        orm_mode = True


class CharityProjectDelete(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime

    class Config:
        orm_mode = True
