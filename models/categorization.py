from sqlalchemy import Column, Integer, String, Boolean
from app.models.base_model import Base

class Categorization(Base):
    __tablename__ = "categorization"

    app_id = Column(Integer, nullable=False, unique=True)
    windows = Column(Boolean, default=False)
    mac = Column(Boolean, default=False)
    linux = Column(Boolean, default=False)
    categories = Column(String)
    genres = Column(String)
    tags = Column(String)
    categorization_id = Column(Integer, primary_key=True, autoincrement=True)
