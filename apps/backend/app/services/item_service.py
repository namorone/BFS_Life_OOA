import json
from datetime import date
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models.item import Item
from app.db.models.warranty import Warranty
from app.repositories.category_repo import CategoryRepository
from app.repositories.item_repo import ItemRepository
from app.schemas.item import DashboardStats, ItemCreate


class ItemService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.item_repository = ItemRepository(db)
        self.category_repository = CategoryRepository(db)

    async def create_item(self, payload: str, photo: UploadFile | None) -> Item:
        try:
            data = ItemCreate.model_validate(json.loads(payload))
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid item payload: {exc}",
            ) from exc

        if data.category_id is not None:
            category = await self.category_repository.get_by_id(data.category_id)
            if category is None:
                raise HTTPException(status_code=404, detail="Category not found")

        photo_path = await self._save_photo(photo) if photo else None
        item = Item(
            name=data.name,
            description=data.description,
            purchase_date=data.purchase_date,
            purchase_price=data.purchase_price,
            category_id=data.category_id,
            photo_path=photo_path,
        )

        if data.warranty is not None:
            item.warranty = Warranty(
                provider=data.warranty.provider,
                expiry_date=data.warranty.expiry_date,
                notes=data.warranty.notes,
            )

        item = await self.item_repository.create(item)
        full_item = await self.item_repository.get_with_relations(item.id)
        if full_item is None:
            raise HTTPException(status_code=500, detail="Failed to load created item")
        return full_item

    async def get_dashboard_stats(self) -> DashboardStats:
        today = date.today()
        total_items = await self.item_repository.count_total_items()
        active_warranties = await self.item_repository.count_active_warranties(today)
        expiring_soon = await self.item_repository.count_expiring_soon(
            today, settings.warranty_expiring_days
        )
        return DashboardStats(
            total_items=total_items,
            active_warranties=active_warranties,
            expiring_soon=expiring_soon,
        )

    async def _save_photo(self, photo: UploadFile) -> str:
        media_root = Path(settings.media_root)
        media_root.mkdir(parents=True, exist_ok=True)
        suffix = Path(photo.filename or "photo").suffix or ".jpg"
        file_name = f"{uuid4().hex}{suffix}"
        destination = media_root / file_name
        with destination.open("wb") as buffer:
            buffer.write(await photo.read())
        return str(destination)
