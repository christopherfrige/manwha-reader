from fastapi import APIRouter, Depends

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.schemas.chapter import GetChapterPagesResponse
from src.domain.use_cases.chapter.get_chapter_pages import GetChapterPagesUseCase

router = APIRouter(prefix="/v1/chapters", tags=["v1"])


@router.get("/{chapter_id}", response_model=GetChapterPagesResponse, status_code=200)
def get_chapter_pages(chapter_id: int, db=Depends(UnitOfWork)):
    return GetChapterPagesUseCase(db).execute(chapter_id)
