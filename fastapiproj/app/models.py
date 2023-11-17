from sqlalchemy import String, Boolean, Integer, Column, text, TIMESTAMP
from databse import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, index=True)
    question_1 = Column(String)
    question_2 = Column(String)
    question_3 = Column(String)
    question_4 = Column(String)
