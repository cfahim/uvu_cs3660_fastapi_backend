
from models.user_model import User
from repositories.rbac_repository import RbacRepository
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self, 
                 user_repository: UserRepository,
                 rbac_repository: RbacRepository,
                 logger): 
        self.user_repository = user_repository
        self.rbac_repository = rbac_repository
        self.logger = logger
    
    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all_users()
    
    async def get_all_users_with_roles(self) -> list[User]:
        return await self.user_repository.get_all_users_with_roles()
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.user_repository.get_user_by_id(user_id)
    
    async def set_user_roles(self, user: User, roles: list[str]) -> None:
        user.roles.clear()
        for role in roles:
            role_obj = await self.rbac_repository.get_only_role_by_name(role)
            if role_obj:
                user.roles.append(role_obj)
        self.user_repository.commit_and_refresh(user)
