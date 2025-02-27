from fastapi import FastAPI
import httpx
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

@app.get("/api/films")
async def get_films():
    """Fetches Star Wars films from SWAPI and returns the JSON response."""
    url = "https://swapi.dev/api/films/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()  # Returns the JSON response
        return {"error": f"Failed to fetch films: {response.status_code}"}
    
# Define request model
class LoginRequest(BaseModel):
    username: str
    password: str

# Function to verify login from users.json
def verify_login(username: str, password: str) -> bool:
    try:
        with open("./db/users.json", "r") as file:
            data = json.load(file)
            for user in data["users"]:
                if user["username"] == username and user["password"] == password:
                    return True
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="User file not found")
    return False

# Login endpoint
@app.post("/api/login")
def login(request: LoginRequest):
    if verify_login(request.username, request.password):
        return {"success": True}
    raise HTTPException(status_code=401, detail="Invalid credentials")
