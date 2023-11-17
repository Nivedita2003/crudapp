from pydantic import BaseModel

class Question(BaseModel):
    question: str
    option1: str 
    option2: str
    option3: str
    option4: str

class Response(BaseModel):
    question_id: int
    username: str
    email: str 
    answer: str
    