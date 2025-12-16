from typing import Type, List, Dict, Any, Union
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.inspection import inspect


from restaurant.database.sql import sql_db as db


class BaseController:

    model = None

    def __init__(self, model=None):
        if model:
            self.model = model
        if self.model is None:
            raise NotImplementedError(
                "The 'model' attribute must be defined in the subclass."
            )

    def _get_primary_key_name(self) -> str:
        return inspect(self.model).primary_key[0].name

    def find_all(self) -> List:
        return db.session.execute(db.select(self.model)).scalars().all()

    def find_by_key(self, key: Any):
        return db.session.get(self.model, key)

    def find_by_filters(self, **kwargs) -> List:
        return (
            db.session.execute(db.select(self.model).filter_by(**kwargs))
            .scalars()
            .all()
        )

    def create(self, data: Dict[str, Any]):
        try:
            instance = self.model(**data)
            db.session.add(instance)
            db.session.commit()
            return instance
        except IntegrityError:
            db.session.rollback()
            return None
        except SQLAlchemyError:
            db.session.rollback()
            return None

    def update(self, key: Any, data: Dict[str, Any]):
        instance = self.find_by_key(key)
        if not instance:
            return None

        try:
            for k, v in data.items():
                if v is not None and hasattr(instance, k):
                    setattr(instance, k, v)

            db.session.commit()
            return instance
        except SQLAlchemyError:
            db.session.rollback()
            return None

    def delete_by_key(self, key: Any) -> bool:
        instance = self.find_by_key(key)
        if not instance:
            return False

        try:
            db.session.delete(instance)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False
