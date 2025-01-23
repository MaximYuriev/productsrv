from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api.routers.product import product_router
from src.ioc import AppProvider

container = make_async_container(AppProvider())

app = FastAPI(title="Product Service")
app.include_router(product_router)

setup_dishka(container, app)
