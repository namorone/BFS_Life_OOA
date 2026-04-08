from fastapi import APIRouter
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])

fake_categories = [
    {"id": 1, "name": "Electronics"},
    {"id": 2, "name": "Furniture"},
]


@router.get("", response_model=list[Category])
def get_categories():
    return fake_categories


@router.post("", response_model=Category)
def create_category(payload: CategoryCreate):
    new_id = max([c["id"] for c in fake_categories]) + 1 if fake_categories else 1
    category = {"id": new_id, "name": payload.name}
    fake_categories.append(category)
    return category


@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, payload: CategoryUpdate):
    for c in fake_categories:
        if c["id"] == category_id:
            c["name"] = payload.name
            return c
    return {}


@router.delete("/{category_id}")
def delete_category(category_id: int):
    global fake_categories
    fake_categories = [c for c in fake_categories if c["id"] != category_id]
    return {"ok": True}
