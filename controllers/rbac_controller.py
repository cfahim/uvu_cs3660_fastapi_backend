from fastapi import APIRouter, Depends, HTTPException, Request
from dependency_injector.wiring import Provide, inject

from containers import Container
from models.rbac_model import PermissionEnum
from schemas.rbac_schema import PutRoleSchemaRequest, RoleSchema
from services.auth_service import AuthorizationService
from services.rbac_service import RbacService


router = APIRouter(prefix="/api/rbac", tags=["Authentication"])

@router.get("/roles", response_model=list[RoleSchema])
@inject
async def get_roles(request: Request,
                    rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                    auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN,PermissionEnum.RBACREAD])
    return await rbac_service.get_all_roles_with_permissions()

@router.get("/roles/{role_id}", response_model=RoleSchema)
@inject
async def get_role(request: Request, 
                   role_id: int, 
                   rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                   auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN,PermissionEnum.RBACREAD])

    role = await rbac_service.get_role_by_id(role_id)
    if not role:
        return {"message": "Role not found"}
    return role

@router.put("/roles/{role_id}/permissions", response_model=RoleSchema)
@inject
async def update_role_permissions(request: Request,
                                  role_id: int, 
                                  permissions: PutRoleSchemaRequest,
                                  rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                                  auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN,PermissionEnum.RBACWRITE])

    role = await rbac_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    role = await rbac_service.update_role_permissions(role, permissions.role_permissions)
    if not role:
        return {"message": "Failed to update role permissions"}

    # Update role permissions logic here
    # For now, just return the updated role
    return role