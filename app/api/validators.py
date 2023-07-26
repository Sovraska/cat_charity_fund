from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    charity_project = await charity_project_crud.get_charity_project_by_name(name, session)
    if charity_project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await charity_project_crud.get(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден!'
        )
    return charity_project


async def check_is_invested_amount_zero(
    charity_project: CharityProject
) -> None:
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_is_full_amount_gt_invested_amount(
    charity_project: CharityProject,
    obj_in: CharityProjectUpdate
) -> None:
    if obj_in.full_amount:
        if obj_in.full_amount < charity_project.invested_amount:
            raise HTTPException(
                status_code=400,
                detail='Нельзя Установить Общую сумму ниже накопленной!'
            )


async def check_is_closed_project(
    charity_project: CharityProject,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
