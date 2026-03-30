from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.category_repo import CategoryRepository


class CategoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.repository = CategoryRepository(db)

    async def list_categories(self):
        return await self.repository.list_all()
