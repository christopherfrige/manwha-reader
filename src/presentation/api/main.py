import uvicorn
from fastapi import FastAPI

from src.presentation.api.v1.routers.api import router as v1_router
from src.infrastructure.config import SETTINGS

app = FastAPI()

app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run("src.presentation.api.main:app", host="0.0.0.0", reload=SETTINGS.app_environment=="development", port=8000)