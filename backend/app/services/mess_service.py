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
                    name=created_mess.name,
                    city=created_mess.city,
                    type=created_mess.type,
                    monthly_price=created_mess.monthly_price,
                    address=created_mess.address,
                    description=created_mess.description,
                    contact_number=created_mess.contact_number
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

    def fetch_messes(self):
        """
        Fetch all active messes from the database.

        This method retrieves mess records that are not soft-deleted (`is_deleted=False`) 
        from the database using the repository. Each mess is serialized into a response 
        schema format before being returned.

        Returns:
            Success response containing a list of active messes in `MessResponse` format.
            If no messes are found, returns an empty list in the response.

        Error:
            - If a database error occurs, returns a server error response with DB error details.
            - If any other unexpected exception occurs, returns a general failure response.

        """
        try:
            with self.repo.db.begin():
                active_messes = self.repo.get_active_messes()
                if not active_messes:
                    return self.resp_builder.build_success_response(data=[])

                mess_data = [
                    MessResponse(
                        mess_id=mess.mess_id,
                        name=mess.name,
                        city=mess.city,
                        type=mess.type,
                        monthly_price=mess.monthly_price,
                        address=mess.address,
                        description=mess.description,
                        contact_number=mess.contact_number
                    ).model_dump()
                    for mess in active_messes
                ]

                return self.resp_builder.build_success_response(data=mess_data)

        except SQLAlchemyError as db_err:
            self.repo.db.rollback()
            return self.resp_builder.build_server_error_response(messages.FAILED_TO_FETCH_MESSES, {"error": str(db_err)})

        except Exception as exc:
            self.repo.db.rollback()
            return self.resp_builder.build_server_error_response(messages.FAILED_TO_FETCH_MESSES, {"error": str(exc)})
