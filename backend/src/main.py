import uvicorn
from app import app
from settings import settings

if __name__ == "__main__":
    uvicorn.run(app, host=settings.SERVER_HOST, port=8001)

