from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import uvicorn
import colorama

from log import logger

from users.views import users_rt
from core.views import db_rt

from settings import settings
from core.db import Base

from app import app

load_dotenv()

colorama.init(autoreset=True)


async def startup():
    logger.info("Site is running.")


async def shutdown():
    logger.info("Site is closing")


def create_main_router():
    router = APIRouter(prefix="/api")
    router.include_router(users_rt)
    router.include_router(db_rt)
    return router


app.include_router(create_main_router())


@app.get(
    "/",
    response_class=JSONResponse
)
async def start_page():
    return {"status-code": 200, "page": "Main page"}


if __name__ == "__main__":
    logger.info("Starting server")
    uvicorn.run(app, host=settings.SERVER_HOST, port=8001)
