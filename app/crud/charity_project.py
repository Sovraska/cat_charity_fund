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
            select(CharityProject).where(
                CharityProject.name == name
            )
        )
        charity_project = charity_project.scalars().first()
        return charity_project


charity_project_crud = CRUDCharityProject(CharityProject)
