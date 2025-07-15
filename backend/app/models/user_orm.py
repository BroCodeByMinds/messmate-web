from sqlalchemy import Boolean, Column, Integer, String
from app.models.base import Base
from app.constants.db_tables import SCHEMA_MASTER, TABLE_USERS

class UserORM(Base):
    __tablename__ = TABLE_USERS
    __table_args__ = {"schema": SCHEMA_MASTER}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)
    role = Column(String, default="student")  # 'student', 'mess_owner', 'admin'
    is_google_user = Column(Boolean, default=False)
