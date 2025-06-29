from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base
from app.models.mixins import TimestampMixin, SoftDeleteMixin

class CustomBase(TimestampMixin, SoftDeleteMixin):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=CustomBase)
