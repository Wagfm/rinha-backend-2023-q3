from flask import Blueprint

from controllers.persons import PersonsController


class PersonsRoute(Blueprint):
    def __init__(self, name: str, controller: PersonsController, **kwargs):
        super().__init__(name, __name__, **kwargs)
        self.post("/pessoas")(controller.create_person)
        self.get("/pessoas/<string:id>")(controller.read_person)
        self.get("/pessoas")(controller.read_by_search_term)
        self.get("/contagem-pessoas")(controller.read_count)
