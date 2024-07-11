import datetime
from typing import Annotated

from pydantic import BaseModel, field_validator, Field


class CreatePersonDto(BaseModel):
    apelido: Annotated[str | None, Field(default=None, validate_default=True)]
    nome: Annotated[str | None, Field(default=None, validate_default=True)]
    nascimento: Annotated[str | None, Field(default=None, validate_default=True)]
    stack: Annotated[list[str] | None, Field(default=None, validate_default=True)]

    @field_validator("apelido")
    @classmethod
    def validate_nickname(cls, nickname: str | None) -> str:
        if nickname is None:
            raise ValueError("Nickname cannot be null")
        if len(nickname) > 32:
            raise ValueError("Nickname must be less than 32 characters")
        return nickname

    @field_validator("nome")
    @classmethod
    def validate_name(cls, name: str | None) -> str:
        if name is None:
            raise ValueError("Name cannot be null")
        if len(name) > 100:
            raise ValueError("Name must be less than 100 characters")
        return name

    @field_validator("nascimento")
    @classmethod
    def validate_birthday(cls, birthday: str | None) -> str:
        if birthday is None:
            raise ValueError("Birthday must be specified")
        try:
            datetime.datetime.strptime(birthday, "%Y-%m-%d")
            return birthday
        except Exception:
            raise ValueError("Birthday must be in YYYY-MM-DD format")

    @field_validator("stack")
    @classmethod
    def validate_stack(cls, stack: list[str] | None) -> list[str] | None:
        if stack is None:
            return stack
        if any([len(element) > 32 for element in stack]):
            raise ValueError("Stack elements must be less than 32 characters")
        return stack
