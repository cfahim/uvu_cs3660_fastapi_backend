from fastapi import FastAPI
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from controllers import login_controller, swapi_controller
from middleware.auth_middleware import AuthMiddleware


app = FastAPI()

app.add_middleware(AuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)



app.include_router(login_controller.router)
app.include_router(swapi_controller.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health")
def health():
    return {"message": "Ok"}

