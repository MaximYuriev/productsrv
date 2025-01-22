class BaseId:
    _id = 0

    def __init__(self):
        self._id = self._create_new_id()

    @classmethod
    def _create_new_id(cls) -> int:
        cls._id += 1
        return cls._id

    @property
    def id(self) -> int:
        return self._id
