from . import schemas
from .security import get_password_hash

# Database mokada
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "hashed_password": get_password_hash("testpassword"),
        "disabled": False,
    },
        "cesar": {
        "username": "cesar",
        "full_name": "Cesar Sousa",
        "email": "cesar@email.com",
        "hashed_password": get_password_hash("103020"),
        "disabled": False,
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)