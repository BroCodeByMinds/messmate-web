from sqlalchemy.orm import Session
from app.models.mess_orm import MessORM
from app.repositories.mess_repository import MessRepository
from app.schemas.mess import MessCreate, MessResponse
from app.utils.response_builder import ResponseBuilder
from app.constants import messages
from sqlalchemy.exc import SQLAlchemyError


class MessService:
    def __init__(self, db: Session, resp_builder: ResponseBuilder):
        self.repo = MessRepository(db)
        self.resp_builder = resp_builder
    
    def create_mess(self, mess: MessCreate):
        try:
            with self.repo.db.begin():
                if self.repo.get_mess_by_name(mess.name):
                    return self.resp_builder.build_conflict_response(messages.MESS_ALREADY_EXISTS)
                
                mess_data = mess.model_dump()
                mess = MessORM(**mess_data, created_by=1)

                created_mess = self.repo.create_mess(mess)

            return self.resp_builder.build_created_response(
                messages.MESS_REGISTERED_SUCCESSFULLY,
                MessResponse(
                    mess_id=created_mess.mess_id,
                    name=created_mess.name
                ).model_dump()
            )

        except SQLAlchemyError as db_error:
            self.repo.db.rollback()
            return self.resp_builder.build_server_error_response(
                messages.MESS_REGISTRATION_FAILED,
                {"db_error": str(db_error)}
            )

        except Exception as exc:
            self.repo.db.rollback()
            return self.resp_builder.build_server_error_response(
                messages.MESS_REGISTRATION_FAILED,
                {"error": str(exc)}
            )
