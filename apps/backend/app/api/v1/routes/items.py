from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.item import ItemRead
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemRead, status_code=201)
async def create_item(
    payload: str = Form(...),
    photo: UploadFile | None = File(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ItemService(db)
    return await service.create_item(
        payload=payload,
        photo=photo,
        current_user=current_user,
    )
