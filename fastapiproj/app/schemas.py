from pydantic import BaseModel

class Users(BaseModel):
    name: str
    email:str
    question_1: str 
    question_2: str
    question_3: str
    question_4: str