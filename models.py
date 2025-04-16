from sqlalchemy import Column, Integer, Float
from database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    feature_0 = Column(Float)
    feature_1 = Column(Float)
    feature_2 = Column(Float)
    feature_3 = Column(Float)
    feature_4 = Column(Float)
    feature_5 = Column(Float)
    feature_6 = Column(Float)
    feature_7 = Column(Float)
    feature_8 = Column(Float)
    feature_9 = Column(Float)
    result = Column(Integer)
