from fastapi import APIRouter, Form
from backend.filemodels import ItemResponse, StatusResponse
from backend.db import create_user, get_user_by_username, get_user_hash, \
    get_user_id_by_hash, get_items, get_user, update_item, delete_item
from backend.models.items import ItemsListResponse
from backend.models.users import RegisterRequest, UserResponse, LoginRequest, LoginResponse
from fastapi import Depends, HTTPException, status
from docs.responses import already_register_responses, incorrect_creditionals
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

token_scheme = HTTPBearer(scheme_name="user_hash_auth")
router = APIRouter(prefix="/api")

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(token_scheme)) -> int:
    token = credentials.credentials
    user_id = get_user_id_by_hash(token)

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    return user_id

# ===== User =====
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

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
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")

    user_hash = get_user_hash(payload.username, payload.password)
    return LoginResponse(user_id=user_id, user_hash=user_hash)


# ===== Items =====
@router.get("/items", response_model=ItemsListResponse,
            summary="Получение списка всех Items",
            description="Принимает на вход user_hash и возвращает список Item, если у пользователя есть доступ.\n\n"
            "user_hash можно получить при помощи метода /api/login",
            tags=["Items"])
def get_items_list(_: int = Depends(get_current_user_id)):
    items_list = get_items()
    return ItemsListResponse(items=items_list)


@router.post("/items/update", response_model=StatusResponse)
def api_update_item(item_id: int = Form(...), name: str = Form(...), description: str = Form(...)):
    update_item(item_id, name, description)
    return StatusResponse(status="ok")


@router.post("/items/delete", response_model=StatusResponse)
def api_delete_item(item_id: int = Form(...)):
    delete_item(item_id)
    return StatusResponse(status="ok")
