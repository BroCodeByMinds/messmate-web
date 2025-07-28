from functools import wraps
from sqlalchemy.exc import SQLAlchemyError

def db_error_handler(failure_message: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except SQLAlchemyError as db_err:
                self.repo.db.rollback()
                return self.resp_builder.build_server_error_response(failure_message, {"error": str(db_err)})
            except Exception as exc:
                self.repo.db.rollback()
                return self.resp_builder.build_server_error_response(failure_message, {"error": str(exc)})
        return wrapper
    return decorator
