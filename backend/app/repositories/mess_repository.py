from sqlalchemy.orm import Session

from app.models.mess_orm import MessORM

class MessRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_mess_by_name(self, name: str) -> MessORM | None:
        return self.db.query(MessORM).filter(MessORM.name == name).first()
    
    def create_mess(self, user: MessORM) -> MessORM:
        self.db.add(user)
        self.db.flush()  # Ensures ID is generated
        self.db.refresh(user)
        return user
    
    def get_active_messes(self):
        return self.db.query(MessORM).filter(MessORM.is_deleted.is_(False)).all()
