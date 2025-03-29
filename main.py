from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from fastapi.middleware.cors import CORSMiddleware

from controllers import login_controller, swapi_controller
from config import settings

from middleware.api_gateway_middleware import ApiGatewayAuthMiddleware
from middleware.auth_middleware import AuthMiddleware
from schemas.message_schema import MessageResponse


app = FastAPI(title="CS3660 Backend Project", version="1.0.0")

app.add_middleware(AuthMiddleware)
# CORS is handled through API Gateway, only need for testing locally
if settings.app_env == "local":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,  # Allow requests from React frontend
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
        allow_headers=["*"],  # Allow all headers
    )

app.add_middleware(ApiGatewayAuthMiddleware)  # Middleware to check API token





app.include_router(login_controller.router)
app.include_router(swapi_controller.router)

@app.get("/", response_model=MessageResponse)
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/health", response_model=MessageResponse)
def health():
    return {"message": "Ok"}



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="CS3660 Backend Project",
        routes=app.routes,
    )

    
    openapi_schema["openapi"] = "3.0.1"
    
    openapi_schema["paths"] = {
        path.rstrip("/") if path != "/" else path: data 
        for path, data in openapi_schema["paths"].items() if path != ""
    }
   
    for schema_name, schema in openapi_schema["components"]["schemas"].items():
        if "properties" in schema:
            for field_name, field in schema["properties"].items():
                if "anyOf" in field:
                    field["type"] = "string"  # Replace 'anyOf' with AWS-supported format
                    field["nullable"] = True
                    del field["anyOf"]
    
    for path, methods in openapi_schema["paths"].items():
        for method, data in methods.items():
            if "operationId" in data:
                data["operationId"] = "".join(
                    word.capitalize() for word in data["operationId"].split("_")
                )  # Convert to CamelCase

    """"
    "openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
        }
    }

    for path, methods in openapi_schema["paths"].items():
        if path != "/api/login":  # Skip authentication for login endpoint
            for method in methods:
                methods[method]["security"] = [{"BearerAuth": []}]"
    """

    # Ensure All Response Models Have `"type": "object"`
    for schema_name, schema in openapi_schema["components"]["schemas"].items():
        if "type" not in schema:
            schema["type"] = "object"  # Add type explicitly

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi