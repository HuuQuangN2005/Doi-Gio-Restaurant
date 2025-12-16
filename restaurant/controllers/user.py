import hashlib
from typing import Dict, Any, Union

from restaurant.database.sql.models.user import User
from restaurant.controllers.base import BaseController


class UserController(BaseController):

    model = User

    def __init__(self):
        super().__init__(model=self.model)

    def _hash_password(self, password: str) -> str:
        return hashlib.md5(password.encode("utf-8")).hexdigest()

    def authenticate(self, username: str, password: str) -> Union[User, None]:
        hashed_password = self._hash_password(password)
        users = self.find_by_filters(username=username, password=hashed_password)

        if users:
            return users[0]
        else:
            return None

    def create(self, data: Dict[str, Any]) -> Union[User, None]:
        if "password" in data:
            data["password"] = self._hash_password(data["password"])

        return super().create(data)

    def update(self, key: Any, data: Dict[str, Any]) -> Union[User, None]:
        if "password" in data and data["password"]:
            data["password"] = self._hash_password(data["password"])

        return super().update(key, data)
