from sqlalchemy import Column, Integer, ForeignKey
from app.models.base_model import Base

class Performance(Base):
    __tablename__ = "performance"

    sales_sales_id = Column(Integer, ForeignKey("sales.salesid"), nullable=False)
    positive = Column(Integer)
    negative = Column(Integer)
    score_rank = Column(Integer)
    recommend = Column(Integer)
    id = Column(Integer, primary_key=True, autoincrement=True)
