from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    description: str
    owner_id: int


class ItemsListResponse(BaseModel):
    items: list[Item]


class ItemResponse(BaseModel):
    item_id: int


class ItemCreateRequest(BaseModel):
    name: str
    description: str
    owner_id: str


class ItemUpdateRequest(BaseModel):
    item_id: int
    name: str
    description: str


class ItemDeleteRequest(BaseModel):
    item_id: int