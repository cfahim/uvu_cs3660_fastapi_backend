from db.db import DatabaseFactory
from models.rbac_model import Permission, Role, RolePermission

from sqlalchemy.orm import Session, joinedload

class RbacRepository:
    def __init__(self, db: DatabaseFactory):
        self.db: Session = db.get_session()

    async def get_all_roles_with_permissions(self) -> list[Role] | None:
        return ( 
            self.db.query(Role)
            .options(
                joinedload(Role.role_permissions)
                .joinedload(RolePermission.permission)
            )
            .all()
        )
    
    async def get_role_by_id(self, role_id: int) -> Role | None:
        return (
            self.db.query(Role)
            .options(
                joinedload(Role.role_permissions)
                .joinedload(RolePermission.permission)
            )
            .filter(Role.id == role_id)
            .first()
        )
    
    async def get_permissions_by_name(self, permissions: list[str]) -> list[Permission] | None:
        return (
            self.db.query(Permission)
            .filter(Permission.name.in_(permissions))
            .all()
        )
    
    def commit_and_refresh(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)