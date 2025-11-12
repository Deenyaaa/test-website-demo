from pydantic import BaseModel
from typing import Optional

class StatusResponse(BaseModel):
    status: str

class UserResponse(StatusResponse):
    user_id: Optional[int] = None

class ItemResponse(StatusResponse):
    item_id: Optional[int] = None