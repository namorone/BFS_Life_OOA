from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category


class CategoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_all(self) -> list[Category]:
        result = await self.db.execute(select(Category).order_by(Category.name.asc()))
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Category | None:
        return await self.db.get(Category, category_id)
