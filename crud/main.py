from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from databases import Database
import logging
logging.basicConfig(filename='fastapi.log', level=logging.DEBUG)

# Database configuration
DATABASE_URL = "postgresql://postgres:123456@127.0.0.1/postgres"

database = Database(DATABASE_URL)

# SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

class Response(Base):
    __tablename__ = "user_responses"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer)
    answer = Column(String)

# Create tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get the database session
async def get_db():
    db = database
    try:
        yield db
    finally:
        db.disconnect()

# HTML Form for User Information and Skin Questionnaire
user_info_form = """
<body>
    <h1>Enter Your Details</h1>
    <form method="post" action="/user-info">
        <label for="name">Name:</label>
        <input type="text" name="name" required>
        
        <label for="email">Email:</label>
        <input type="email" name="email" required>

        <div class="questionnaire">
            <h2>Skin Questionnaire</h2>
            <label>What is your skin type?</label>
            <select name="question_1" required>
                <option value="Oily">Oily</option>
                <option value="Dry">Dry</option>
                <option value="Combination">Combination</option>
            </select>

<label>How often do you cleanse your face in a day?</label>
<select name="question_2" required>
    <option value="Once">Once</option>
    <option value="Twice">Twice</option>
    <option value="More than twice">More than twice</option>
</select>

<label>Do you experience breakouts or acne often?</label>
<select name="question_3" required>
    <option value="Yes">Yes</option>
    <option value="No">No</option>
</select>

<label>What is your primary skin concern?</label>
<select name="question_4" required>
    <option value="Wrinkles">Wrinkles</option>
    <option value="Dark spots">Dark spots</option>
    <option value="Redness">Redness</option>
</select>


        </div>

        <button type="submit">Submit</button>
    </form>
</body>
"""

# HTML Template for Viewing Records
view_records_template = """
<body>
    <h1>View Records</h1>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Question ID</th>
                <th>Answer</th>
            </tr>
        </thead>
        <tbody>
            {% for record in records %}
                <tr>
                    <td>{{ record[0] }}</td>
                    <td>{{ record[1] }}</td>
                    <td>{{ record[2] }}</td>
                    <td>{{ record[3] }}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content=user_info_form, status_code=200)

@app.post("/user-info", response_class=HTMLResponse, include_in_schema=True)
async def user_info(
    name: str = Form(...),
    email: str = Form(...),
    question_1: str = Form(...),
    question_2: str = Form(...),
    question_3: str = Form(...),
    question_4: str = Form(...),
    db: Database = Depends(get_db)
):
    try:
        logging.info(f"Received form data: name={name}, email={email}, question_1={question_1}, question_2={question_2}, question_3={question_3}, question_4={question_4}")

        async with db.transaction():
            # Save user's name and email to the database
            print("Inside transaction block")
            await database.execute(User.__table__.insert().values({"name": name, "email": email}))

            # Retrieve the user ID after insertion
            query = User.__table__.select().where(User.name == name, User.email == email)
            user_row = await database.fetch_one(query)
            user_id = user_row['id']

            # Save the user's answers to the questionnaire
            responses = [
                Response(user_id=user_id, question_id=1, answer=question_1),
                Response(user_id=user_id, question_id=2, answer=question_2),
                Response(user_id=user_id, question_id=3, answer=question_3),
                Response(user_id=user_id, question_id=4, answer=question_4),
            ]
            await database.execute(Response.__table__.insert().values(responses))

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(e)  # Print the exception to the console as well
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return HTMLResponse(content="<h1>Thank You for Completing the Questionnaire!</h1><a href='/view-records'>View Records</a>", status_code=200)


@app.get("/view-records", response_class=HTMLResponse)
async def view_records(db: Database = Depends(get_db)):
    async with db.transaction():
        records = []  # Define records outside of the try block
        try:
            # Retrieve records from the database
            query = User.__table__.join(Response.__table__)
            records = await database.fetch_all(query)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return HTMLResponse(content=view_records_template, status_code=200, media_type="text/html", context={"records": records})


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
