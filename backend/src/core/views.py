from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from log import logger
from core.db import init_db


db_rt = APIRouter(prefix="/db", tags=["Database"])


@db_rt.post(
    "/init",
    response_class=JSONResponse
)
async def init_database():
    try:
        await init_db()
        return {"status": 200}
    except Exception as e:
        logger.critical(e)
        print(e)
    return HTTPException(500, "Database initialize went wrong.")