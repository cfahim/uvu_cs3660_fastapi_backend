from fastapi import HTTPException

from repositories.user_repository import UserRepository


class AuthorizationService:
    def __init__(self, user_repository):
        self.user_repository: UserRepository = user_repository

    def assert_permissions(self, request, permissions):
        if not request.state.jwt_payload:
            raise HTTPException(status_code=403, detail="Forbidden")
        

        # for possible caching later
        user_permissions = self._get_user_permissions(request.state.jwt_payload["user"]["username"])
        
        # check if user has at least one of the permissions
        if any(permission.value in user_permissions for permission in permissions):
            return
                
        raise HTTPException(status_code=403, detail="Forbidden")

    def _get_user_permissions(self, username):
        user = self.user_repository.get_user_by_username_with_roles(username)
        if not user:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        # get all permissions for the user
        permissions = set()
        for role in user.roles:
            for permission in role.role_permissions:
                permissions.add(permission.permission.name)
        
        return permissions
    
    def assert_roles(self, request, roles):
        if not request.state.jwt_payload:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        user = self.user_repository.get_user_by_username(request.state.jwt_payload["user"]["username"])
        if not user:
            raise HTTPException(status_code=403, detail="Forbidden")

        # check if user has at least one of the roles
        if any(user.has_role(role) for role in roles):
            return            
        
        raise HTTPException(status_code=403, detail="Forbidden")

