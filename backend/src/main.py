from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse

from dotenv import load_dotenv
import uvicorn
import colorama

from log import logger

from users.views import users_rt
from core.views import db_rt

from settings import settings
from core.db import Base


load_dotenv()

colorama.init(autoreset=True)

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")


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
    print(Base.metadata.tables)
    uvicorn.run(app, host=settings.SERVER_HOST, port=8001)
