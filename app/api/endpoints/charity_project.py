from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists,
    check_charity_project_name_duplicate,
    check_is_closed_project,
    check_is_full_amount_gt_invested_amount,
    check_is_invested_amount_zero,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment_service import investment

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await investment(new_charity_project, session)
    return new_charity_project


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)

    await check_is_full_amount_gt_invested_amount(charity_project, obj_in)
    await check_is_closed_project(charity_project)
    await check_charity_project_name_duplicate(obj_in.name, session)
    return await charity_project_crud.update(charity_project, obj_in, session)


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_is_invested_amount_zero(charity_project)
    await check_is_closed_project(charity_project)
    return await charity_project_crud.remove(charity_project, session)
