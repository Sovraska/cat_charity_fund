from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class DonationBase(BaseModel):
    full_amount: int
    comment: Optional[str]


class DonationCreate(DonationBase):
    @validator('full_amount')
    def check_full_amount(cls, value):
        if not isinstance(value, int):
            raise ValueError(
                'full_amount не число'
            )
        if value <= 0:
            raise ValueError(
                'full_amount не может быть ниже 0'
            )
        return value


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationAdmin(DonationBase):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: datetime = None

    class Config:
        orm_mode = True
