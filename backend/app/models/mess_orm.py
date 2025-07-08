from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text
from app.constants.db_tables import MESSES, SCHEMA_MASTER
from app.models.base import Base

class MessORM(Base):
    __tablename__ = MESSES
    __table_args__ = {"schema": SCHEMA_MASTER}

    mess_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)  # Veg, Non-Veg, Both
    monthly_price = Column(Integer, nullable=False)
    address = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    contact_number = Column(String(15), nullable=True)
    created_by = Column(Integer, nullable=False)