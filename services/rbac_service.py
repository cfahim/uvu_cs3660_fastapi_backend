from models.rbac_model import Permission, Role, RolePermission
from models.user_model import User
from repositories.rbac_repository import RbacRepository
from schemas.rbac_schema import PutPermissionSchemaRequest


class RbacService:
    def __init__(self, rbac_repository: RbacRepository): 
        self.rbac_repository = rbac_repository
    
    async def get_all_roles_with_permissions(self) -> list[Role]:
        return await self.rbac_repository.get_all_roles_with_permissions()
    
    async def get_role_by_id(self, role_id: int) -> Role | None:
        return await self.rbac_repository.get_role_by_id(role_id)
    
    async def get_role_by_name(self, role_name: str) -> Role | None:
        return await self.rbac_repository.get_role_by_name(role_name)
    
    async def get_or_put_role(self, role_name: str, user: User) -> Role | None:
        # Check if the role already exists
        role = await self.rbac_repository.get_role_by_name(role_name)
        
        if not role:
            # If not, create a new role
            role = Role(name=role_name, created_by_id=user.id)
            self.rbac_repository.commit_and_refresh(role)
        
        return role
    
    async def get_all_permissions(self) -> list[Permission]:
        return await self.rbac_repository.get_all_permissions()
    
    async def get_permission_by_id(self, permission_id: int) -> Permission | None:
        return await self.rbac_repository.get_permission_by_id(permission_id)
    
    async def get_or_put_permission(self, permission_name: str, user: User) -> Permission | None:
        # Check if the permission already exists
        permission = await self.rbac_repository.get_permissions_by_name([permission_name])
        
        if not permission:
            # If not, create a new permission
            permission = Permission(name=permission_name, created_by_id=user.id)
            self.rbac_repository.commit_and_refresh(permission)
        
        return permission
    
    async def update_permission(self, 
                                permission: Permission, 
                                updated_permission: PutPermissionSchemaRequest,
                                user: User) -> Permission | None:
        # Update the permission name and created_by_id
        permission.name = updated_permission.name
        permission.created_by_id = user.id
        self.rbac_repository.commit_and_refresh(permission)

    
    async def delete_permission(self, permission: Permission):
        self.rbac_repository.delete(permission)
    
    
    async def update_role_permissions(self, role: Role, permissions: list[str], user: User) -> Role | None:
        # Clear existing permissions
        role.role_permissions.clear()

        permissions = await self.rbac_repository.get_permissions_by_name(permissions)        
        
        # Add new permissions
        for permission in permissions:            
            role_permission = RolePermission(
                role_id=role.id,
                permission_id=permission.id,                
                created_by_id=user.id
            )
            role.role_permissions.append(role_permission)

        # Commit changes to the database
        self.rbac_repository.commit_and_refresh(role)
        
        # Return the updated role with permissions
        return role
        