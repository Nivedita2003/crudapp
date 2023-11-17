from asyncpg import ForeignKeyViolationError
from sqlalchemy import String, ForeignKey, Integer, Column, text, TIMESTAMP
from sqlalchemy.orm import relationship
from databse import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    option1 = Column(String)
    option2 = Column(String)
    option3 = Column(String)
    option4 = Column(String)
    responses = relationship("Response", back_populates="question")

# Define the responses table
class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    username = Column(String)
    email = Column(String)
    answer = Column(String)
    question = relationship("Question", back_populates="responses")