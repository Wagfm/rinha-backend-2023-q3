from typing import Any, Sequence
from psycopg import Cursor


class DictRowFactory:
    def __init__(self, cursor: Cursor[Any]):
        self._fields = [column.name for column in cursor.description] if cursor.description is not None else []

    def __call__(self, values: Sequence[Any]) -> dict[str, Any]:
        return dict(zip(self._fields, values))
