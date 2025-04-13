from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from models.base_model import Base
from models.rbac_model import RoleEnum, user_roles


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(512), nullable=False)

    roles = relationship('Role', secondary=user_roles, backref='users')

    def has_role(self, role_name: RoleEnum) -> bool:
        return any(role.name == role_name for role in self.roles)
