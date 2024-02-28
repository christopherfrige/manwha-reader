from fastapi import APIRouter, Depends

from src.infrastructure.persistence.unit_of_work import UnitOfWork
from src.domain.use_cases.manwha.get_all_manwhas import GetAllManwhasUseCase
from src.domain.use_cases.manwha.get_manwha import GetManwhaUseCase
from src.domain.schemas.manwha import GetAllManwhasResponse, GetManwhaResponse

router = APIRouter(prefix="/v1/chapters", tags=["v1"])


@router.get("/{chapter_id}", status_code=200)
def get_chapter_pages(chapter_id: int, db = Depends(UnitOfWork)):
    
    return 
