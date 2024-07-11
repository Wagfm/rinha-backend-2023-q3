from pydantic import BaseModel


class ReadPersonDto(BaseModel):
    id: str
    apelido: str
    nome: str
    nascimento: str
    stack: list[str]
