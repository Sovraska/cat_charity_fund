import datetime
from typing import List

from sqlalchemy import select

from app.models import CharityProject, Donation


async def check_is_not_full_amount(model, session) -> List:
    """getting unclosed instances of some model"""
    investments = await session.execute(
        select(model).where(
            model.fully_invested == False  # noqa: E712
        )
    )
    return investments.scalars().all()


async def transfer_invested_amount_lt(transfer_to, transfer_from, session):
    """called when investment less or equal then the newly created object"""
    transfer_to.invested_amount += transfer_from.full_amount - transfer_from.invested_amount
    transfer_from.invested_amount = transfer_from.full_amount
    transfer_from.fully_invested = True
    transfer_from.close_date = datetime.datetime.utcnow()
    if transfer_to.full_amount == transfer_to.invested_amount:
        transfer_to.fully_invested = True
        transfer_to.close_date = datetime.datetime.utcnow()

    session.add(transfer_to)
    session.add(transfer_from)
    await session.commit()
    await session.refresh(transfer_to)
    return transfer_to


async def transfer_invested_amount_gt(transfer_to, transfer_from, session):
    """called when investment grater then the newly created object"""
    transfer_from.invested_amount += transfer_to.full_amount - transfer_to.invested_amount
    transfer_to.invested_amount = transfer_to.full_amount
    transfer_to.fully_invested = True
    transfer_to.close_date = datetime.datetime.utcnow()
    if transfer_from.full_amount == transfer_from.invested_amount:
        transfer_from.fully_invested = True
        transfer_from.close_date = datetime.datetime.utcnow()
    session.add(transfer_to)
    session.add(transfer_from)
    await session.commit()
    await session.refresh(transfer_to)
    return transfer_to


async def investment(new_object, session):
    """Investment Algorithm Universal function for two types of Objects

    CharityProject and Donation
    """
    if isinstance(new_object, CharityProject):
        model = Donation
    else:
        model = CharityProject

    investments = await check_is_not_full_amount(model, session)
    result = []
    if not investments:
        return
    more_to_invest = investments[0].full_amount - investments[0].invested_amount
    for investment_obj in investments:
        if new_object.fully_invested:
            if new_object.full_amount == new_object.invested_amount:
                break

        await session.refresh(investment_obj)
        await session.refresh(new_object)

        if new_object.full_amount < more_to_invest:
            added_amount = await transfer_invested_amount_gt(
                new_object,
                investment_obj,
                session
            )
            result.append(added_amount.invested_amount)
            await session.refresh(investment_obj)
            more_to_invest = investment_obj.full_amount - investment_obj.invested_amount

        else:
            added_amount = await transfer_invested_amount_lt(
                new_object,
                investment_obj,
                session
            )
            result.append(added_amount.invested_amount)
            await session.refresh(investment_obj)
            more_to_invest = investment_obj.full_amount - investment_obj.invested_amount
