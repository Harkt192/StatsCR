from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from core.db import init_db
from log import logger


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
    return HTTPException(500, "Database initialize went wrong.")