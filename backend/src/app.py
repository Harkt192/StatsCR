from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import fastapi
from dotenv import load_dotenv
import uvicorn
import colorama
import logging
import os

from request import CrApiManager
from log import logger


load_dotenv()

colorama.init(autoreset=True)

app = FastAPI()


ApiManager = CrApiManager(
    apikey=os.getenv("APIKEY"),
    address="https://api.clashroyale.com/v1"
)


@app.get("/", response_class=JSONResponse)
async def root(request: Request):
    params = {
        "request": request,
        "title": "Главная страница"
    }
    logger.info("Вход на Главную страницу")
    return {"status_code": 200}


@app.get("/api/player/{player_tag}", response_class=JSONResponse)
async def say_hello(request: Request, player_tag: str):
    logger.info(f"Request Player Запрос к пользователю #{player_tag}")
    return ApiManager.getPlayerInfo(player_tag)


@app.get("/api/player/{player_tag}/battlelog", response_class=JSONResponse)
async def say_hello(request: Request, player_tag: str):
    logger.info(f"Request Battlelog к пользователю #{player_tag}")
    return ApiManager.getPlayerBattleLog(player_tag)
