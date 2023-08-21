from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router,
    donation,
    user_router,
    google_router,
)

main_router = APIRouter()
main_router.include_router(
    charity_project_router, prefix="/charity_project", tags=["charity_projects"]
)
main_router.include_router(donation, prefix="/donation", tags=["donations"])
main_router.include_router(google_router, prefix="/google", tags=["Google"])
main_router.include_router(user_router)
