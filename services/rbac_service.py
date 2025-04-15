from models.rbac_model import Role, RolePermission
from repositories.rbac_repository import RbacRepository


class RbacService:
    def __init__(self, rbac_repository: RbacRepository): 
        self.rbac_repository = rbac_repository
    
    async def get_all_roles_with_permissions(self) -> list[Role]:
        return await self.rbac_repository.get_all_roles_with_permissions()
    
    async def get_role_by_id(self, role_id: int) -> Role | None:
        return await self.rbac_repository.get_role_by_id(role_id)
    
    async def update_role_permissions(self, role: Role, permissions: list[str]) -> Role | None:
        # Clear existing permissions
        role.role_permissions.clear()

        permissions = await self.rbac_repository.get_permissions_by_name(permissions)        
        
        # Add new permissions
        for permission in permissions:            
            role_permission = RolePermission(
                role_id=role.id,
                permission_id=permission.id,                
                created_by_id=1
            )
            role.role_permissions.append(role_permission)

        # Commit changes to the database
        self.rbac_repository.commit_and_refresh(role)
        
        # Return the updated role with permissions
        return role
        