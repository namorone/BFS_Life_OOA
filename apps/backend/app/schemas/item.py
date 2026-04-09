from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.category import CategoryRead


class WarrantyCreate(BaseModel):
    provider: str | None = None
    expiry_date: date
    notes: str | None = None


class WarrantyRead(WarrantyCreate):
    id: int

    model_config = {"from_attributes": True}


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    category_id: int | None = None
    purchase_date: date | None = None
    purchase_price: Decimal | None = Field(default=None, ge=0)
    description: str | None = None
    warranty: WarrantyCreate | None = None


class ItemRead(BaseModel):
    id: int
    name: str
    description: str | None
    purchase_date: date | None
    purchase_price: Decimal | None
    photo_path: str | None
    category: CategoryRead | None
    warranty: WarrantyRead | None

    model_config = {"from_attributes": True}


class DashboardStats(BaseModel):
    total_items: int
    active_warranties: int
    expiring_soon: int
