from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from databse import get_db
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from databse import engine
from schemas import Question
from schemas import Response
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='postgres', user='postgres',
                                password='123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database succesfully connected')
        break
    except Exception as error:
        print('connection failed')
        print('error:', error)
        time.sleep(3)

app = FastAPI()

models.Base.metadata.create_all(bind= engine)

@app.get("/")
def posts():
    return {"message": "this is working"}

@app.post("/questions/")
def create_question(question_data: Question,db: Session=Depends(get_db)):
    question = models.Question(**question_data.dict())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

@app.get("/questions/")
def get_questions(db: Session= Depends(get_db)):
    all_question= db.query(models.Question).all()
    return all_question

@app.post("/responses/")
def create_response(response_data: Response, db: Session=Depends(get_db)):
    response = models.Response(**response_data.dict())
    db.add(response)
    db.commit()
    db.refresh(response)
    return response

@app.get("/responses/")
def get_responses(db: Session=Depends(get_db)):
    all_response= db.query(models.Response).all()
    return all_response







