from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationAdmin, DonationCreate, DonationDB
from app.services.investment_service import investment

router = APIRouter()


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(donation, session, user)
    await investment(new_donation, session)
    return new_donation


@router.get(
    "/",
    response_model=list[DonationAdmin],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def my(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_my_donations(user, session)
