from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str
