from pydantic import BaseModel

class ItemsListResponse(BaseModel):
    items: list