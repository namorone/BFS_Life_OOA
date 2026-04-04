from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.category import CategoryRead
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryRead])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    service = CategoryService(db)
    return await service.list_categories()
