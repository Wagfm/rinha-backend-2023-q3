from dataclasses import dataclass, asdict, fields
from datetime import date
from uuid import UUID


@dataclass(frozen=True)
class PersonModel:
    id: UUID
    nickname: str
    name: str
    birth_date: date
    stack: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> "PersonModel":
        valid_data = {field.name: data.get(field.name) for field in fields(cls)}
        return cls(**valid_data)

    def to_dict(self, include_none=True) -> dict:
        data = asdict(self)
        if include_none:
            return data
        return {key: value for key, value in data.items() if value is not None}

    @classmethod
    def get_fields(cls) -> list[str]:
        return [field.name for field in fields(cls)]
