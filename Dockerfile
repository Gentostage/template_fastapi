# Используем образ Python
FROM python:3.10-slim

# Устанавливаем переменная окружения для предотвращения вывода логов от Python в буферизированный режим
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости проекта и устанавливаем их
COPY poetry.lock pyproject.toml /app/
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копируем исходный код проекта в контейнер
COPY . /app

RUN alembic upgrade head

# Запускаем сервер FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]