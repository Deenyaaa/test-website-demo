from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.db import create_user, get_user_id, add_item, update_item, delete_item, get_items_list

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

# === Web Pages ===
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    items = get_items_list()
    return templates.TemplateResponse("dashboard.html", {"request": request, "items": items})

# === Web Forms Routes ===
@router.post("/register")
def register_user(username: str = Form(...), password: str = Form(...)):
    user_id = create_user(username, password)
    if not user_id:
        raise HTTPException(status_code=400, detail="User exists")
    return RedirectResponse(url="/login", status_code=303)

@router.post("/login")
def login_user(username: str = Form(...), password: str = Form(...)):
    user = get_user_id(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return RedirectResponse(url=f"/dashboard?user_id={user}", status_code=303)

@router.post("/items")
def add_item_route(name: str = Form(...), description: str = Form(...), owner_id: int = Form(...)):
    add_item(name, description, owner_id)
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/items/update")
def update_item_route(item_id: int = Form(...), name: str = Form(...), description: str = Form(...)):
    update_item(item_id, name, description)
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/items/delete")
def delete_item_route(item_id: int = Form(...)):
    delete_item(item_id)
    return RedirectResponse(url="/dashboard", status_code=303)
