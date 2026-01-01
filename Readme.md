# Test Website Demo

Минимальный тестовый веб-сайт для демонстрации навыков автоматизации.
Содержит:
- Регистрацию и авторизацию пользователей
- Cоздание, редактирование, удаление(CRUD)  предметов в базе данных(Items)
- SQLite базу данных
- Простые HTML, CSS страницы

Проект предназначен для запуска и тестирования автоматических сценариев

---

# 🌐 Live Demo
- 🚀 Демо-версия сайта доступна по адресу:
👉 http://185.130.225.146:9000/
- 📗Swagger доступен по адресу:
👉 http://185.130.225.146:9000/swagger
- 📙Redoc доступен по адресу:
👉 http://185.130.225.146:9000/redoc

---

## 🛠 Требования

- Python 3.10+
- pip
- Установленные библиотеки из `requirements.txt`

```txt
fastapi
uvicorn
jinja2
pydantic
python-multipart
```

---

## 📂 Структура проекта

```
test-website-demo/
├─ backend/
│  ├─ main.py         # FastAPI приложение
│  ├─ models/         # Pydantic модели
│  │  ├─ items.py
│  │  ├─ shared.py
│  │  └─ users.py
│  ├─ db.py           # Подключение к SQLite
│  └─ templates/      # HTML страницы
├─ static/            # CSS и JS
├─ docs/              # Документация для swagger
├─ test.db            # SQLite база данных (создаётся автоматически)
├─ requirements.txt
└─ README.md
```

---

## ⚡ Инициализация базы данных

При первом запуске сервера, если `test.db` отсутствует, можно создать базу вручную:

```bash
python init_db.py
```

- Создаст `test.db` с таблицами `users` и `items`.

---

## 💻 Запуск

### Docker

1. Перейдите в директорию с проектом
```bash
cd projectpath
```
2. Соберите Docker-образ
```bash
docker build -t fastapi-app .
```
3. Запустите Docker-образ
```bash
docker run -d -p 8000:8000 fastapi-app
```

### Windows

1. Создайте виртуальное окружение 
```bash
python -m venv envname
```
2. Активируйте виртуальное окружение:

```cmd
.venv\Scripts\activate
```

2. Установите зависимости:

```cmd
pip install -r requirements.txt
```

3. Запустите сервер:

```cmd
uvicorn backend.main:app --reload
```

4. Откройте браузер:

```
http://127.0.0.1:8000/
```

---

### Linux / VPS

1. Создайте виртуальное окружение 
```bash
python3 -m venv myenv
```
2. Активируйте виртуальное окружение (если используете):

```bash
source .venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте базу данных (если ещё нет):

```bash
python init_db.py
```

4. Запустите сервер (для доступа извне укажите `--host 0.0.0.0`):

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

5. На VPS откройте порт 8000 в фаерволе, затем доступно по IP сервера:

```
http://<VPS_IP>:8000/
```

---

## ⚙️ Использование

- **Регистрация:** `/register`
- **Логин:** `/login`
- **Dashboard (CRUD):** `/dashboard`

После регистрации можно авторизоваться и создавать/редактировать/удалять предметы (items).

---
