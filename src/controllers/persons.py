import json
from typing import Any
from uuid import UUID

import psycopg
from flask import Response, request

from dtos.create_person import CreatePersonDto
from services.persons import PersonsService


class PersonsController:
    def __init__(self):
        self._service = PersonsService()

    def create_person(self) -> Response:
        headers = {"Location": f"/pessoas/null"}
        return self._build_json_response({}, 201, headers=headers)
        person_data = request.json
        try:
            create_person_dto = CreatePersonDto(**person_data)
            read_person_dto = self._service.create_person(create_person_dto)
            headers = {"Location": f"/pessoas/{read_person_dto.id}"}
            return self._build_json_response(read_person_dto.model_dump(), 201, headers=headers)
        except ValueError as exception:
            return self._build_json_response({"message": str(exception)}, 400)
        except psycopg.Error as error:
            return self._build_json_response({"message": str(error)}, 422)
        except Exception as exception:
            return self._build_json_response({"message": str(exception)}, 500)

    def read_person(self, id: str) -> Response:
        return self._build_json_response({}, 200)
        try:
            UUID(id, version=4)
        except ValueError:
            return self._build_json_response({"message": "UUID cannot be parsed"}, 400)
        read_person_dto = self._service.read_person(id)
        if read_person_dto is None:
            return self._build_json_response({"message": f"Person {id} not found"}, 404)
        return self._build_json_response(read_person_dto.model_dump(), 200)

    def read_by_search_term(self) -> Response:
        search_term = request.args.get("t")
        if search_term is None:
            return self._build_json_response({}, 400)
        return self._build_json_response([], 200)
        try:
            read_person_dtos = self._service.read_by_search_term(search_term)
            return self._build_json_response([dto.model_dump() for dto in read_person_dtos], 200)
        except Exception as exception:
            return self._build_json_response({"message": str(exception)}, 500)

    def read_count(self):
        n = self._service.read_count()
        return self._build_json_response(n, 200, "text/plain")

    @staticmethod
    def _build_json_response(content: Any, status_code: int, mimetype="application/json", **kwargs) -> Response:
        return Response(json.dumps(content), status_code, mimetype=mimetype, **kwargs)
