from restaurant.utils import Utils
import hashlib

from typing import Dict, Any, Union
from restaurant.models import db
from restaurant.models.sql import User, Employee, UserRole, Table
from restaurant.utils import Utils


class UserService:
    def __init__(self):
        pass

    def get_tables(self) -> list[Table]:
        return Table.query.filter(Table.active == True).all()

    def get_user_by_id(self, id: int) -> Union[User, None]:
        return User.query.get(id)

    def get_user_by_uuid(self, uuid: str) -> Union[User, None]:
        return User.query.filter_by(uuid=uuid).first()

    def hash_password(self, password: str) -> str:
        return hashlib.md5(str(password).encode("utf-8")).hexdigest()

    def authenticate(self, username: str, password: str) -> Union[Employee, None]:

        try:
            hashed_password = self.hash_password(password)
            user = Employee.query.filter_by(
                username=username, password=hashed_password, active=True
            ).first()

            if user:
                Utils.logger.info(
                    f"UserService: Authenticated successfully for: {username}"
                )
                return user

            Utils.logger.warning(f"UserService: Auth failed for: {username}")
            return None
        except Exception as e:
            Utils.logger.error(f"UserService: Auth system error - {str(e)}")
            return None

    def create(self, data: Dict[str, Any]) -> Union[User, None]:

        try:
            email = data.get("email")
            phone = data.get("phone")

            existing = User.query.filter(
                (User.email == email) | (User.phone == phone)
            ).first()
            if existing:
                Utils.logger.warning(
                    f"UserService: Create failed. User already exists!!!"
                )
                return None

            common_args = {
                "name": data.get("name"),
                "address": data.get("address"),
                "gender": data.get("gender"),
                "email": email,
                "phone": phone,
                "role": (
                    UserRole[data.get("role")]
                    if isinstance(data.get("role"), str)
                    else data.get("role")
                ),
                "active": data.get("active", True),
            }

            if data.get("type") == "employee":
                emp_details = data.get("employee_details", {})

                avatar_url = Utils.upload_image(
                    emp_details.get("avatar"), "restaurant/avatars"
                )
                hashed_pw = self.hash_password(emp_details.get("password", "123"))

                new_user = Employee(
                    **common_args,
                    username=emp_details.get("username"),
                    password=hashed_pw,
                    avatar=avatar_url,
                )
            else:
                new_user = User(**common_args)

            db.session.add(new_user)
            db.session.commit()

            Utils.logger.info(
                f"UserService: Successfully created {data.get('type')} - {new_user.uuid}"
            )
            return new_user

        except Exception as e:
            db.session.rollback()
            Utils.logger.error(f"UserService: Error in create - {str(e)}")
            return None

    def update(self, user_id: int, data: Dict[str, Any]) -> Union[User, None]:
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return None

            if "password" in data and data["password"] and isinstance(user, Employee):
                user.password = self.hash_password(data["password"])

            if "avatar" in data and data["avatar"] and isinstance(user, Employee):
                new_url = self.upload_avatar(data["avatar"])
                if new_url:
                    user.avatar = new_url

            for key, value in data.items():
                if key not in ["password", "avatar"] and hasattr(user, key):
                    setattr(user, key, value)

            db.session.commit()
            Utils.logger.info(f"UserService: Updated user ID {user_id}")
            return user

        except Exception as e:
            db.session.rollback()
            Utils.logger.error(f"UserService: Update error - {str(e)}")
            return None


user_service = UserService()
