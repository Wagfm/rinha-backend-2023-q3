from dtos.create_person import CreatePersonDto
from dtos.read_person import ReadPersonDto
from models.person import PersonModel
from repositories.persons import PersonsRepository


class PersonsService:
    def __init__(self):
        self._repository = PersonsRepository()

    def create_person(self, dto: CreatePersonDto) -> ReadPersonDto:
        person_model = self._repository.create_person(dto)
        read_person_dto = self._translate_en_to_br(person_model)
        return read_person_dto

    def read_person(self, id: str) -> ReadPersonDto | None:
        person_model = self._repository.get_person_by_id(id)
        if person_model is None:
            return None
        read_person_dto = self._translate_en_to_br(person_model)
        return read_person_dto

    def read_by_search_term(self, search_term: str) -> list[ReadPersonDto]:
        person_models = self._repository.get_person_by_search_term(search_term)
        read_person_dtos = [self._translate_en_to_br(model) for model in person_models]
        return read_person_dtos

    def read_count(self):
        return self._repository.get_person_count()

    @staticmethod
    def _translate_en_to_br(model: PersonModel) -> ReadPersonDto:
        return ReadPersonDto(**{
            "id": str(model.id),
            "nome": model.name,
            "apelido": model.nickname,
            "nascimento": model.birth_date.strftime("%Y-%m-%d"),
            "stack": model.stack
        })
