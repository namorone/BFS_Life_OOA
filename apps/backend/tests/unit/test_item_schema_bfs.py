import pytest
from pydantic import ValidationError

from app.schemas.item import ItemCreate


def test_bfs_item_schema_accepts_minimal_payload() -> None:
    item = ItemCreate(
        name="Laptop",
        category_id=None,
        purchase_date=None,
        purchase_price=None,
        description=None,
        warranty=None,
    )
    assert item.name == "Laptop"


def test_bfs_item_schema_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        ItemCreate(name="")


def test_bfs_item_schema_rejects_negative_price() -> None:
    with pytest.raises(ValidationError):
        ItemCreate(name="Laptop", purchase_price="-1")
