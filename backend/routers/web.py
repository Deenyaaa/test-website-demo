import os
from fastapi import APIRouter, Request, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from backend import db
from backend.db import create_user, get_user_credentials, add_item, update_item, delete_item, get_items_list

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")


def get_web_user(request: Request) -> dict | None:
    token = request.cookies.get("session")
    if not token:
        return None
    user_id = db.get_user_id_by_hash(token)
    if user_id is None:
        return None
    return db.get_user_info(user_id)


# === Web Pages ===
@router.get("/", response_class=HTMLResponse, tags=["Web"])
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"current_user": get_web_user(request)})

@router.get("/register", response_class=HTMLResponse, tags=["Web"])
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"current_user": get_web_user(request)})

@router.get("/login", response_class=HTMLResponse, tags=["Web"])
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"current_user": get_web_user(request)})

@router.get("/dashboard", response_class=HTMLResponse, tags=["Web"])
def dashboard(request: Request):
    current_user = get_web_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    items = get_items_list()
    return templates.TemplateResponse(request, "dashboard.html", {"current_user": current_user, "items": items})

@router.get("/profile", response_class=HTMLResponse, tags=["Web"])
def profile_page(request: Request):
    current_user = get_web_user(request)
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(request, "profile.html", {"current_user": current_user})

@router.get("/logout", tags=["Web"])
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="session")
    return response


# === Web Forms Routes ===
@router.post("/register", tags=["Web"])
def register_user(username: str = Form(...), password: str = Form(...)):
    user_id = create_user(username, password)
    if not user_id:
        raise HTTPException(status_code=400, detail="User exists")
    return RedirectResponse(url="/login", status_code=303)

@router.post("/login", tags=["Web"])
def login_user(username: str = Form(...), password: str = Form(...)):
    credentials = get_user_credentials(username, password)
    if not credentials:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    _, user_hash = credentials
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(key="session", value=user_hash, httponly=True, samesite="lax")
    return response

@router.post("/profile/change-password", tags=["Web"])
async def change_password(request: Request, old_password: str = Form(...), new_password: str = Form(...)):
    current_user = get_web_user(request)
    if not current_user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    if not db.verify_user_password(current_user["id"], old_password):
        return JSONResponse({"error": "Неверный текущий пароль"}, status_code=400)
    db.update_user_password(current_user["id"], new_password)
    return JSONResponse({"success": True})

@router.post("/profile/upload-avatar", tags=["Web"])
async def upload_avatar(request: Request, avatar: UploadFile = File(...)):
    current_user = get_web_user(request)
    if not current_user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    ext = avatar.filename.rsplit(".", 1)[-1].lower() if "." in avatar.filename else ""
    if ext not in ("png", "jpg", "jpeg"):
        return JSONResponse({"error": "Разрешены только .png, .jpg, .jpeg"}, status_code=400)
    os.makedirs("static/avatars", exist_ok=True)
    path = f"static/avatars/{current_user['id']}.{ext}"
    contents = await avatar.read()
    with open(path, "wb") as f:
        f.write(contents)
    avatar_url = f"/static/avatars/{current_user['id']}.{ext}"
    db.update_user_avatar(current_user["id"], avatar_url)
    return JSONResponse({"avatar_url": avatar_url})

@router.post("/items", tags=["Web"])
def add_item_route(name: str = Form(...), description: str = Form(...), owner_id: int = Form(...)):
    add_item(name, description, owner_id)
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/items/update", tags=["Web"])
def update_item_route(item_id: int = Form(...), name: str = Form(...), description: str = Form(...)):
    update_item(item_id, name, description)
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/items/delete", tags=["Web"])
def delete_item_route(item_id: int = Form(...)):
    delete_item(item_id)
    return RedirectResponse(url="/dashboard", status_code=303)
