from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.mess import MessCreate, MessResponse
from app.services.mess_service import MessService
from app.utils.response_builder import ResponseBuilder
from app.db.database import get_db


router = APIRouter()


def get_response_builder() -> ResponseBuilder:
    return ResponseBuilder()


@router.post("/create", response_model=MessResponse)
def create(
    mess: MessCreate,
    db: Session = Depends(get_db),
    resp_builder: ResponseBuilder = Depends(get_response_builder),
):
    service = MessService(db, resp_builder)
    return service.create_mess(mess)

@router.get("fetch_messes", response_model=MessResponse)
def fetch_messes(db:Session = Depends(get_db), resp_builder:ResponseBuilder = Depends(get_response_builder)):
    service = MessService(db, resp_builder)
    return service.fetch_messes()