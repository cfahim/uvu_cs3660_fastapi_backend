from db.db import DatabaseFactory
from models.user_model import User
from models.rbac_model import Role, RolePermission

from sqlalchemy.orm import Session, joinedload

class UserRepository:
    def __init__(self, db: DatabaseFactory):
        self.db: Session = db.get_session()

    def get_user_by_username_with_roles(self, username: str) -> User:
        return ( 
            self.db.query(User)
            .options(
                joinedload(User.roles)
                .joinedload(Role.role_permissions)
                .joinedload(RolePermission.permission)
            )
            .filter(User.username == username)
            .first()
        )
    
    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()
        
    async def get_all_users(self) -> list[User]:
        return self.db.query(User).all()
    
    async def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()
    
    async def get_all_users_with_roles(self) -> list[User]:
        return ( 
            self.db.query(User)
            .options(
                joinedload(User.roles)
            )
            .all()
        )
    
    def commit_and_refresh(self, instance: User) -> None:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)