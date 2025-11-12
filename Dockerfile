FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Экспонируем порт
EXPOSE 8000

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
