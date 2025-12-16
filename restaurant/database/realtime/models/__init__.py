from restaurant.database.realtime import rdb


class FirebaseModel:
    FIREBASE_NODE = None

    def __init__(self, **kwargs):
        self.key = kwargs.pop("key", None)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def _get_ref(cls):
        if not cls.FIREBASE_NODE:
            raise NotImplementedError("FIREBASE_NODE must be defined in the subclass.")
        return rdb.reference(cls.FIREBASE_NODE)

    def to_dict(self):
        data = {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_") and k != "key"
        }
        return data

    def save(self):
        ref = self._get_ref()
        data = self.to_dict()

        if self.key:
            ref.child(self.key).update(data)
        else:
            if not data:
                return 

            new_ref = ref.push(data) 
            self.key = new_ref.key

    def delete(self):
        if self.key:
            self._get_ref().child(self.key).delete()
            self.key = None

    @classmethod
    def get(cls, key):
        data = cls._get_ref().child(key).get()

        if data:
            return cls(key=key, **data)
        return None

    @classmethod
    def all(cls):
        data = cls._get_ref().get()

        if not data:
            return []

        results = []
        for key, item in data.items():
            if isinstance(item, dict):
                results.append(cls(key=key, **item))
        return results
