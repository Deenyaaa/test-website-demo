from fastapi import APIRouter, Form
from backend.models import UserResponse, ItemResponse, StatusResponse
from backend.db import create_user, get_user, add_item, update_item, delete_item

router = APIRouter()

# === API Routes for Testing ===
@router.post("/register", response_model=UserResponse)
def api_register(username: str = Form(...), password: str = Form(...)):
    user_id = create_user(username, password)
    if user_id:
        return UserResponse(status="ok", user_id=user_id)
    return UserResponse(status="error", user_id=None)

@router.post("/login", response_model=UserResponse)
def api_login(username: str = Form(...), password: str = Form(...)):
    user = get_user(username, password)
    if user:
        return UserResponse(status="ok", user_id=user)
    return UserResponse(status="error", user_id=None)

@router.post("/items", response_model=ItemResponse)
def api_add_item(name: str = Form(...), description: str = Form(...), owner_id: int = Form(...)):
    item_id = add_item(name, description, owner_id)
    return ItemResponse(status="ok", item_id=item_id)

@router.post("/items/update", response_model=StatusResponse)
def api_update_item(item_id: int = Form(...), name: str = Form(...), description: str = Form(...)):
    update_item(item_id, name, description)
    return StatusResponse(status="ok")

@router.post("/items/delete", response_model=StatusResponse)
def api_delete_item(item_id: int = Form(...)):
    delete_item(item_id)
    return StatusResponse(status="ok")
