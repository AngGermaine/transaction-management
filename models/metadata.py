from sqlalchemy import Column, Integer, String, DateTime
from app.models.base_model import Base

class Metadata(Base):
    __tablename__ = "metadata"

    app_id = Column(Integer, nullable=False, unique=True)
    about_the_game = Column(String)
    website = Column(String)
    support_email = Column(String)
    support_url = Column(String)
    developers = Column(String)
    publishers = Column(String)
    release_date = Column(DateTime)
    metadata_id = Column(Integer, primary_key=True, autoincrement=True)
