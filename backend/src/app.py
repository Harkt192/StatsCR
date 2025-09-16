from fastapi import FastAPI

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_methods=["get", "post", "patch"],
    allow_headers=["*"]
)


redis_pool = ConnectionPool.from_url(
    "redis://127.0.0.1:6379",
    max_connections=10,
    decode_responses=True
)


app.state.redis = Redis(connection_pool=redis_pool)
redis_service = app.state.redis


async def shutdown():
    await redis_service.close()
    await redis_pool.disconnect()


app.add_event_handler("shutdown", shutdown)
