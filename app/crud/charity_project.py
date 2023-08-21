from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        charity_project = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return charity_project.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[dict[str, int]]:
        closed_projects = await session.execute(
            select(
                CharityProject.name,
                CharityProject.close_date,
                CharityProject.create_date,
                CharityProject.description,
            ).where(CharityProject.fully_invested.is_(True))
        )
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
