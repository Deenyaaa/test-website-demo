from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend import db
from backend.models import items as item_models, users as user_models
from docs.responses import already_register_responses, incorrect_credentials


token_scheme = HTTPBearer(scheme_name="user_hash_auth")
router = APIRouter(prefix="/api")


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(token_scheme)) -> int:
    token = credentials.credentials
    user_id = db.get_user_id_by_hash(token)

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
    user_id = db.get_user_id_by_username(username)
    user_exists = user_id is not None

    return {"user_id": user_id, "user_exists": user_exists}


@router.post("/register", response_model=user_models.UserResponse, responses=already_register_responses,
             summary="Регистрация нового пользователя",
             description="Проверяет наличие зарегистрированного пользователя с указанным username и регистрирует, если такой не найден\n\n"
             "Принимает username и password в теле запроса и возвращает user_id после успешной регистрации",
             tags=["Users"])
def register_user(payload: user_models.RegisterRequest):
    existing_user_id = db.get_user_id_by_username(payload.username)
    if existing_user_id is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user_id = db.create_user(payload.username, payload.password)

    return user_models.UserResponse(user_id=user_id)


@router.post("/login", response_model=user_models.LoginResponse, responses=incorrect_credentials,
             summary="Получение hash-токена для авторизации пользователя",
             description="Проверяет авторизацию пользователя в системе и возвращает hash-токен авторизации если авторизация пройдена успешно\n\n"
             "Принимает на вход username и password и возвращает user_hash",
             tags=["Users"])
def login(payload: user_models.LoginRequest):
    user_id = db.get_user_id(payload.username, payload.password)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")

    user_hash = db.get_user_hash(payload.username, payload.password)
    return user_models.LoginResponse(user_id=user_id, user_hash=user_hash)


# ===== Items =====
@router.get("/items", response_model=item_models.ItemsListResponse,
            summary="Получение списка всех Items",
            description="Требует Bearer-токен (user_hash) в заголовке Authorization и возвращает список Item, если у пользователя есть доступ.\n\n"
            "Токен можно получить через /api/login",
            tags=["Items"])
def get_items_list(_: int = Depends(get_current_user_id)):
    items_list = db.get_items_list()
    return item_models.ItemsListResponse(items=items_list)


@router.post("/items/add", response_model=item_models.ItemResponse,
             summary="Добавление нового items в систему",
             description="Принимает в теле запроса name, description и owner_id и возвращает item_id в случае успешного добавления",
             tags=["Items"])
def api_create_item(payload: item_models.ItemCreateRequest, _: int = Depends(get_current_user_id)):
    item_id = db.add_item(payload.name, payload.description, payload.owner_id)
    return item_models.ItemResponse(item_id=item_id)


@router.post("/items/update", response_model=item_models.ItemResponse,
             summary="Обновление данных существующего item",
             description="Принимает в теле запроса item_id, обновленные name и description, а возвращает item_id в случае успешного изменения",
             tags=["Items"])
def api_update_item(payload: item_models.ItemUpdateRequest, _: int = Depends(get_current_user_id)):
    db.update_item(payload.item_id, payload.name, payload.description)
    return item_models.ItemResponse(item_id=payload.item_id)


@router.post("/items/delete", response_model=item_models.ItemsListResponse,
             summary="Удаление item по его id",
             description="Принимает в теле запроса item_id и удаляет его. Возвращает список остальных items",
             tags=["Items"])
def api_delete_item(payload: item_models.ItemDeleteRequest, _: int = Depends(get_current_user_id)):
    db.delete_item(payload.item_id)
    items_list = db.get_items()
    return item_models.ItemsListResponse(items=items_list)
