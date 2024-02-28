import uvicorn
from fastapi import FastAPI

from src.presentation.api.v1.routers.manwhas import router as v1_manwhas
from src.presentation.api.v1.routers.chapters import router as v1_chapters
from src.infrastructure.config import SETTINGS

app = FastAPI()

app.include_router(v1_manwhas)
app.include_router(v1_chapters)

if __name__ == "__main__":
    uvicorn.run("src.presentation.api.main:app", host="0.0.0.0", reload=SETTINGS.app_environment=="development", port=8000)