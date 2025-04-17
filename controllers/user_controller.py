
from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject


from containers import Container
from models.rbac_model import PermissionEnum
from schemas.user_schema import PutUserRolesSchemaRequest, UserSchema
from services.auth_service import AuthorizationService
from services.user_service import UserService


router = APIRouter(prefix="/api/users", tags=["Authorization","RBAC"])

@router.get("", response_model=list[UserSchema])
@inject
async def get_users(request: Request,
                     user_service: UserService = Depends(Provide[Container.user_service]),
                     auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.USERREAD])
    return await user_service.get_all_users_with_roles()

@router.get("/{user_id}", response_model=UserSchema)
@inject
async def get_user(request: Request,
                    user_id: int,
                    user_service: UserService = Depends(Provide[Container.user_service]),
                    auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.USERREAD])
    
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.put("/{user_id}/roles", response_model=UserSchema)
@inject
async def put_user_roles(request: Request,
                         user_id: int,
                         set_roles: PutUserRolesSchemaRequest,
                         user_service: UserService = Depends(Provide[Container.user_service]),
                         auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.USERWRITE])
    
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user_service.set_user_roles(user, set_roles.set_roles)
    return user