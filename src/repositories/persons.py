import json
import os
from functools import wraps
from typing import Callable

import psycopg

from database.row_factory import DictRowFactory
from dtos.create_person import CreatePersonDto
from models.person import PersonModel


class PersonsRepository:
    def __init__(self):
        self._connection_info = {
            "host": os.environ["POSTGRES_HOST"],
            "port": os.environ["POSTGRES_PORT"],
            "dbname": os.environ["POSTGRES_DATABASE"],
            "user": os.environ["POSTGRES_USER"],
            "password": os.environ["POSTGRES_PASSWORD"],
            "connect_timeout": 10,
        }
        self._cursor = None
        self._setup_table()

    @staticmethod
    def _with_connection(function: Callable) -> Callable:
        @wraps(function)
        def with_connection(self, *args, **kwargs):
            try:
                connection = psycopg.connect(**self._connection_info, row_factory=DictRowFactory)
                with connection.cursor() as cursor:
                    self._cursor = cursor
                    result = function(self, *args, **kwargs)
            except psycopg.errors.IntegrityError:
                connection.rollback()
                raise
            except Exception:
                connection.rollback()
                raise
            else:
                connection.commit()
            return result

        return with_connection

    @_with_connection
    def create_person(self, dto: CreatePersonDto) -> PersonModel | None:
        create_person_query = """
            INSERT INTO persons (nickname, name, birth_date, stack) VALUES (%s, %s, %s, %s) RETURNING *;
        """
        parameters = [dto.apelido, dto.nome, dto.nascimento, json.dumps(dto.stack)]
        items = self._cursor.execute(create_person_query.encode(), parameters)
        inserted_person = items.fetchone()
        if inserted_person is None:
            return None
        return PersonModel.from_dict(inserted_person)

    @_with_connection
    def get_person_by_id(self, id: str) -> PersonModel | None:
        get_person_by_id_query = """
            SELECT * FROM persons WHERE id = %s;
        """
        parameters = [id]
        items = self._cursor.execute(get_person_by_id_query.encode(), parameters)
        found_person = items.fetchone()
        if found_person is None:
            return None
        return PersonModel.from_dict(found_person)

    @_with_connection
    def get_person_by_search_term(self, search_term: str) -> list[PersonModel]:
        get_person_by_search_term_query = """
            SELECT * FROM persons WHERE searchable ILIKE %s;
        """
        parameters = [f"%{search_term}%"]
        items = self._cursor.execute(get_person_by_search_term_query.encode(), parameters)
        found_person = items.fetchall()
        return [PersonModel.from_dict(person) for person in found_person]

    @_with_connection
    def get_person_count(self) -> int:
        get_person_count_query = """
            SELECT COUNT(*) FROM persons;
        """
        result = self._cursor.execute(get_person_count_query.encode())
        return result.fetchone()["count"]

    @_with_connection
    def _setup_table(self) -> None:
        try:
            self._cursor.execute("""CREATE EXTENSION IF NOT EXISTS "uuid-ossp";""")
            self._cursor.execute("""CREATE EXTENSION IF NOT EXISTS "pg_trgm";""")
            self._cursor.execute("""
                CREATE OR REPLACE FUNCTION generate_searchable(_name VARCHAR, _nickname VARCHAR, _stack JSON)
                    RETURNS TEXT AS $$
                    BEGIN
                    RETURN _name || _nickname || _stack;
                    END;
                $$ LANGUAGE plpgsql IMMUTABLE;
            """)
        except psycopg.Error:
            pass
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                id UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                nickname VARCHAR(32) UNIQUE NOT NULL,
                birth_date DATE NOT NULL,
                stack JSON NOT NULL,
                searchable TEXT GENERATED ALWAYS AS ( generate_searchable(name, nickname, stack) ) STORED 
            );
        """)
        self._cursor.execute("""
            CREATE INDEX IF NOT EXISTS persons_search_index 
                ON PUBLIC.persons USING GIST(searchable PUBLIC.gist_trgm_ops);
        """)
