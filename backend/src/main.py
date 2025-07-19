from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
import uvicorn
import colorama
import logging
import os

from request import CrApiManager
from log import logger

from core.db import init_db
from users.views import users_rt

from settings import settings


load_dotenv()

colorama.init(autoreset=True)

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")


def create_main_router():
    router = APIRouter(prefix="/api")
    router.include_router(users_rt)
    return router


app.include_router(create_main_router())


@app.get("/", response_class=JSONResponse)
async def start_page(request: Request):
    return {"status-code": 200}


@app.get("/init", response_class=JSONResponse)
async def init_database(request: Request):
    await init_db()
    return {"status-code": 200}


if __name__ == "__main__":
    logger.info("Starting server")
    uvicorn.run(app, host=settings.SERVER_HOST, port=8001)


# ApiManager = CrApiManager(
#     apikey=os.getenv("APIKEY"),
#     address="https://api.clashroyale.com/v1"
# )
#
#
# @app.get("/", response_class=JSONResponse)
# async def root(request: Request):
#     params = {
#         "request": request,
#         "title": "Главная страница"
#     }
#     logger.info("Вход на Главную страницу")
#     return {"status_code": 200}
#
#
# @app.get("/api/player/{player_tag}", response_class=JSONResponse)
# async def say_hello(request: Request, player_tag: str):
#     logger.info(f"Request Player Запрос к пользователю #{player_tag}")
#     return ApiManager.getPlayerInfo(player_tag)
#
#
# @app.get("/api/player/{player_tag}/battlelog", response_class=JSONResponse)
# async def say_hello(request: Request, player_tag: str):
#     logger.info(f"Request Battlelog к пользователю #{player_tag}")
#     return ApiManager.getPlayerBattleLog(player_tag)
