from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = CategoryRepository(db)

    async def list_categories(self):
        return await self.repository.list_all()

    async def create_category(self, payload: CategoryCreate):
        return await self.repository.create(payload)

    async def update_category(self, category_id: int, payload: CategoryUpdate):
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        return await self.repository.update(category, payload)

    async def delete_category(self, category_id: int):
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        await self.repository.delete(category)
