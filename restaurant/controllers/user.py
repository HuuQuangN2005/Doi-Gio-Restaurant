import hashlib
from restaurant.database.sql.models.user import User


class UserController:
    def __init__(self):
        pass

    def authenticate(self, username, password):
        password = hashlib.md5(password.encode("utf-8")).hexdigest()

        return User.query.filter(
            User.username.__eq__(username), User.password.__eq__(password)
        ).first()

    def find_by_uuid(self, uuid: str):
        return User.query.get(str(uuid))

    def find_by_id(self, id: int):
        return User.query.get(int(id))
    
    
