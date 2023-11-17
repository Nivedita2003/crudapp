from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from databse import get_db
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from databse import engine
from schemas import Users
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

@app.post("/user")
def create(user: Users,db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user")
def get(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users

