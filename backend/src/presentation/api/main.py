import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.domain.exceptions.server import BadGatewayException
from src.presentation.api.exception_handlers import (
    bad_gateway_exception_handler,
    bad_request_exception_handler,
    conflict_exception_handler,
    general_exception_handler,
    not_acceptable_exception_handler,
    not_found_exception_handler,
)
from src.domain.exceptions.client import (
    BadRequestException,
    ConflictException,
    NotAcceptableException,
    NotFoundException,
)
from src.presentation.api.v1.routers.manwhas import router as v1_manwhas
from src.presentation.api.v1.routers.chapters import router as v1_chapters
from src.presentation.api.v1.routers.scrapers import router as v1_scrapers
from src.presentation.api.v1.routers.readers import router as v1_readers
from src.infrastructure.config import SETTINGS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_manwhas)
app.include_router(v1_chapters)
app.include_router(v1_scrapers)
app.include_router(v1_readers)


app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(ConflictException, conflict_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BadGatewayException, bad_gateway_exception_handler)
app.add_exception_handler(NotAcceptableException, not_acceptable_exception_handler)


if __name__ == "__main__":
    uvicorn.run(
        "src.presentation.api.main:app",
        host="0.0.0.0",
        reload=SETTINGS.app_environment == "development",
        port=8000,
    )
