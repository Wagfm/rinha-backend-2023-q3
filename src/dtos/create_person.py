import datetime

from pydantic import BaseModel, field_validator


class CreatePersonDto(BaseModel):
    apelido: str
    nome: str
    nascimento: str
    stack: list[str]

    @field_validator("apelido")
    @classmethod
    def validate_nickname(cls, nickname: str) -> str:
        if len(nickname) > 32:
            raise ValueError("Nickname must be less than 32 characters")
        return nickname

    @field_validator("nome")
    @classmethod
    def validate_name(cls, name: str) -> str:
        if len(name) > 100:
            raise ValueError("Name must be less than 100 characters")
        return name

    @field_validator("nascimento")
    @classmethod
    def validate_birthday(cls, birthday: str) -> str:
        try:
            datetime.datetime.strptime(birthday, "%Y-%m-%d")
            return birthday
        except Exception:
            raise ValueError("Birthday must be in YYYY-MM-DD format")

    @field_validator("stack")
    @classmethod
    def validate_stack(cls, stack: list[str]) -> list[str]:
        if any([len(element) > 32 for element in stack]):
            raise ValueError("Stack elements must be less than 32 characters")
        return stack
