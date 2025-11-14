from fastapi import APIRouter, Form
from backend.filemodels import ItemResponse, StatusResponse
from backend.db import create_user, get_user, add_item, update_item, delete_item, get_user_by_username, get_user_hash
from backend.models.users import RegisterRequest, UserResponse, LoginRequest, LoginResponse
from fastapi import HTTPException
from docs.responses import already_register_responses, incorrect_creditionals

router = APIRouter(prefix="/api")

# === API Routes for Testing ===
@router.get("/user",
    summary="Проверка существования пользователя",
    description=(
        "Проверяет, существует ли пользователь с указанным username\n\n"
        "Принимает username в query-параметре и возвращает user_id (если найден) и флаг user_exists"
    ),
    tags=["Users"])
def get_user_id(username: str):
    user_id = get_user_by_username(username)
    user_exists = user_id is not None

    return {"user_id": user_id, "user_exists": user_exists}


@router.post("/register", response_model=UserResponse, responses=already_register_responses,
             summary="Регистрация нового пользователя",
             description="Проверяет наличие зарегистрированного пользователя с указанным username и регистрирует, если такой не найден\n\n"
             "Принимает username и password в теле запроса и возвращает user_id после успешной регистрации",
             tags=["Users"])
def resister_user(payload: RegisterRequest):
    existing_user_id = get_user_by_username(payload.username)
    if existing_user_id:
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = create_user(payload.username, payload.password)

    return UserResponse(user_id=user_id)


@router.post("/login", response_model=LoginResponse, responses=incorrect_creditionals,
             summary="Получение hash-токена для авторизации пользователя",
             description="Проверяет авторизацию пользователя в системе и возвращает hash-токен авторизации если авторизация пройдена успешно\n\n"
             "Принимает на вход username и login и возвращает user_hash",
             tags=["Users"])
def login(payload: LoginRequest):
    user_id = get_user(payload.username, payload.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Incorrect login or password")

    user_hash = get_user_hash(payload.username, payload.password)
    return LoginResponse(user_id=user_id, user_hash=user_hash)

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
