from models.user_model import User

class UserRepository:
    def __init__(self, db):
        self.db = db.get_session()

    
    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()
        
    
    