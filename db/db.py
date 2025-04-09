from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import settings


class DatabaseFactory:
    def __init__(self):
        self.engine = create_engine(settings.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db: Session = None

    def close_session(self):
        self.db.close()

    def get_session(self):
        if not self.db or not self.db.is_active:
            self.db = self.SessionLocal()
            
        return self.db      
        

