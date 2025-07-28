from sqlalchemy.orm import Session
from app.models.mess_orm import MessORM
from app.repositories.mess_repository import MessRepository
from app.schemas.mess import MessCreate, MessResponse
from app.utils.response_builder import ResponseBuilder
from app.constants import messages
from sqlalchemy.exc import SQLAlchemyError
from app.decorators.db_error_handler import db_error_handler

class MessService:
    def __init__(self, db: Session, resp_builder: ResponseBuilder):
        self.repo = MessRepository(db)
        self.resp_builder = resp_builder
    
    @db_error_handler(messages.MESS_REGISTRATION_FAILED)
    def create_mess(self, mess: MessCreate):
        """
        Create a new mess in the system.

        This method first checks if a mess with the same name already exists. 
        If not, it creates a new MessORM object and persists it to the database.
        The created mess details are returned in the success response.

        Parameters:
            mess (MessCreate): Pydantic schema containing mess details to be created.

        Returns:
            Success response with mess details if creation is successful.
            Conflict response if a mess with the same name already exists.

        Exceptions:
            Any SQLAlchemy or unexpected exception is handled by the @db_error_handler decorator,
            which rolls back the transaction and returns a server error response.
        """
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
    

    @db_error_handler(messages.FAILED_TO_FETCH_MESSES)
    def fetch_messes(self):
        """
        Fetch all active (non-deleted) messes from the database.

        This method queries all mess records where `is_deleted` is False
        and returns a list of mess details in the response format.

        Returns:
            Success response with a list of active messes.
            Empty list if no active messes are found.

        Exceptions:
            Any SQLAlchemy or unexpected exception is handled by the @db_error_handler decorator,
            which rolls back the transaction and returns a server error response.
        """
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