from sqlalchemy import Column, Integer, Float
from database import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True)
    principal = Column(Float)
    rate = Column(Float)
    tenure = Column(Integer)
    emi = Column(Float)