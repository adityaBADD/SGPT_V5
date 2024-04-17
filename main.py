from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from fastapi.responses import HTMLResponse

app = FastAPI()

class User(BaseModel):
    name: str
    email: EmailStr
    password: str

# In-memory "database" of user profiles
users_db = []

@app.get("/")
async def root():
    return HTMLResponse("""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI User Management</title>
    </head>
    <body>
        <h1>User Management API</h1>
        <ul>
            <li><a href="/docs">Interactive API docs (Swagger UI)</a></li>
            <li><a href="/redoc">Alternative API docs (ReDoc)</a></li>
        </ul>
    </body>
</html>
""")

@app.get("/users", response_model=List[User])
async def get_all_users():
    return users_db

@app.get("/users/", response_model=User)
async def get_user_by_name(name: str = Query(...)):
    user = next((user for user in users_db if user["name"].lower() == name.lower()), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=User, status_code=201)
async def create_user(user: User):
    user_data = user.dict()
    users_db.append(user_data)
    return user_data

@app.delete("/users/", response_model=dict)
async def delete_user(name: str = Query(...)):
    global users_db
    initial_length = len(users_db)
    users_db = [user for user in users_db if user["name"].lower() != name.lower()]
    if len(users_db) == initial_length:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User '{name}' deleted successfully"}
