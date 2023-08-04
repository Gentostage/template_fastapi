from fastapi import FastAPI

from app.api import metric


def create_app():
    app = FastAPI()

    # Подключение роутеров
    app.include_router(metric.router)

    return app


app = create_app()
