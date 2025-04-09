from sqlalchemy import Column, Integer, String

from models.base_model import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    password_hash = Column(String(512), nullable=False)

    def __init__(self, username: str, name: str, password_hash: str):
        self.username = username
        self.name = name        
        self.password_hash = password_hash