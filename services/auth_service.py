from fastapi import HTTPException


class AuthorizationService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

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

