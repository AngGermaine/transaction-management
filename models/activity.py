from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base_model import Base

class Activity(Base):
    __tablename__ = "activity"

    app_id = Column(Integer, ForeignKey("games.appid"), nullable=False)
    estimated_owners = Column(String)
    peak_ccu = Column(String)
    average_playtime = Column(Integer)
    median_playtime = Column(Integer)
    activity_id = Column(Integer, primary_key=True, autoincrement=True)
