from fastapi import FastAPI, Body, Request, HTTPException, Header, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from random import randint
from typing import List, Dict
import bcrypt
import logging
app = FastAPI()

class StudentBase(BaseModel):
    id: str
    name: str
class StudentPublic(StudentBase):
    enroll : List[Dict] = []
class StudentCreate(StudentBase):
    password: str
class Subject(BaseModel):
    id: str
    name: str
    grade: str
def hashPassword(password:str):
    password = password.encode("utf-8")
    return bcrypt.hashpw (password, bcrypt.gensalt())

def verifyPassword(plainPassword, hashedPassword):
    return bcrypt.checkpw(plainPassword.encode("utf-8"),hashedPassword)

oauth2_scheme = OAuth2PasswordBearer (tokenUrl="token")
token_user = {}
students_db = {
    "1": {
        "id": "1",
        "name" : "Alice",
        "enroll" : [],
        "password" : hashPassword("NoHotFood")
    },
    "2": {
        "id": "2",
        "name" : "James",
        "enroll" : [],
        "password" : hashPassword("NoColdFood")
    },
}

def gen_token(id:str):
    for token in token_user:
        if token_user[token] == id:
            return token 
    token = "%020x" %(randint(0, 0xffffffffffffffffffff))
    while token in token_user:
        token = "%020x" %(randint(0, 0xffffffffffffffffffff))
    token_user[token] = id
    return token

def verify_token(token:str):
    token = token.lower()
    if token in token_user:
        return token_user[token]
    return None

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("token"):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization[len("token"):].strip()
    id = verify_token(token)
    if not id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_record = students_db.get(id)
    if not user_record:
        raise HTTPException(status_code=401, detail="User not found")
    return user_record

@app.get("/student/all", response_model=List[StudentPublic])
def getAllStudents():
    studentList = []
    try:
        for sid, data in students_db.items():
            studentInfo = {
                "id": sid,
                "name": data["name"],
                "enroll": data["enroll"]
            }
            studentList.append(studentInfo)
        return studentList
    except Exception as e:
        logging.error(f"Error fetching all students: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/student/new")
def addStudent(student:StudentCreate):
    if student.id in students_db:
        return {"details":"Student already exist"}
    students_db[student.id] = {
        "id": student.id,
        "name": student.name,
        "password": hashPassword(student.password),
        "enroll": []
    }
    return {"message": "Student created succesfully"}

@app.post("/student/login")
def login(id: str = Body(...), password: str = Body(...)):
    user_record = students_db.get(id)
    if not user_record:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verifyPassword(password, user_record["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    token = gen_token(user_record["id"])
    return {"access_token": token, "token_type":"token"}

@app.get("/studentinfo")
def studentInfo(current_student: dict = Depends(get_current_user)):
    return {"message" : f"Hello, {current_student['name']}! You are authenticated."}

@app.post("/student/enroll")
def enrollSubject(subject: Subject, current_student: dict = Depends(get_current_user)):
    for enrolled_subject in current_student["enroll"]:
        if enrolled_subject["id"] == subject.id:  
            return {"message":"Subject already exists"}
    current_student["enroll"].append(subject.dict())
    return {
        "id": subject.id,
        "name": subject.name,
        "grade": subject.grade
    }

@app.get("/student/enrollments")
def getEnrolledSubjects(current_student: dict = Depends(get_current_user)):
    if not current_student["enroll"]:
        raise HTTPException(status_code=404, detail="No enrolled subjects found")
    
    return current_student["enroll"]

@app.post("/student/logout")
def logout(current_user: dict = Depends(get_current_user)):
    id = current_user["id"]
    for token in token_user:
        if token_user[token] == id:
            del token_user[token]
            break
    return {"message": f"See you, {current_user['name']}! You are logged out."}

