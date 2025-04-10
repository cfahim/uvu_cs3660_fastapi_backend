import enum
from sqlalchemy import Column, ForeignKey, Integer, Enum as SqlEnum, Table
from models.base_model import Base


class RoleName(enum.Enum):
    ADMIN = "admin"
    USERADMIN = "useradmin"
    SWAPIREAD = "swapiread"

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(
        SqlEnum(RoleName, native_enum=False, values_callable=lambda obj: [e.value for e in obj]),
        unique=True,
        nullable=False
    )


user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
)
