from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject

from containers import Container
from models.rbac_model import Role, RoleName
from models.user_model import User
from schemas.swapi_schema import FilmResponse
from services.swapi_service import SWAPIService

def get_current_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

def require_role(required_role: RoleName):
    def checker(user: User = Depends(get_current_user)):
        if not user.has_role(required_role):
            raise HTTPException(status_code=403, detail="Forbidden") # 404 good choice as well here if we want to hide the resource
        return user
    return checker

router = APIRouter(prefix="/api/swapi/films", tags=["swapi","films"])

@router.get("", response_model=FilmResponse)
@inject
async def films(
    swapi_service: SWAPIService = Depends(Provide[Container.swapi_service]),
    current_user: User = Depends(require_role(RoleName.SWAPIREAD))
):
    return await swapi_service.get_all_films()
