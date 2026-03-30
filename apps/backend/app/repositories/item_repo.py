from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.db.models.item import Item
from app.db.models.warranty import Warranty


class ItemRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, item: Item) -> Item:
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def get_with_relations(self, item_id: int) -> Item | None:
        query = (
            select(Item)
            .options(joinedload(Item.category), joinedload(Item.warranty))
            .where(Item.id == item_id)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def count_total_items(self) -> int:
        result = await self.db.execute(select(func.count(Item.id)))
        return int(result.scalar_one() or 0)

    async def count_active_warranties(self, today: date) -> int:
        result = await self.db.execute(
            select(func.count(Warranty.id)).where(Warranty.expiry_date >= today)
        )
        return int(result.scalar_one() or 0)

    async def count_expiring_soon(self, today: date, days: int) -> int:
        deadline = today + timedelta(days=days)
        result = await self.db.execute(
            select(func.count(Warranty.id)).where(
                Warranty.expiry_date >= today,
                Warranty.expiry_date <= deadline,
            )
        )
        return int(result.scalar_one() or 0)
