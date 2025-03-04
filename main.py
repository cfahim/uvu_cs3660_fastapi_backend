from fastapi import FastAPI
import httpx
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from controllers import login_controller


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(login_controller.router)

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
