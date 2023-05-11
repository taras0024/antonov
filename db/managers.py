import datetime
import os
import sqlite3
import sys

import pandas as pd
from colorama import Fore, Back

from constants import DB_NAME, DATETIME_FORMAT, PROJECT_DIR
from db.models import (
    Factory,
    Building,
    RepairOrganization,
    Contract,
    RelationType
)
from exceptions import RelationException
from utils import row_to_dict, colored_print, colored_input


class ModelManager:
    models_map = {
        'factory': Factory.__annotations__,
        'building': Building.__annotations__,
        'repair_organization': RepairOrganization.__annotations__,
        'contract': Contract.__annotations__
    }

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.fields_info = self.models_map[table_name]

    @staticmethod
    def process_relation(field_type: type, field: str) -> list | None:
        if field_type != RelationType:
            return None

        table = field.replace('_id', '')
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {table}")
            rows = cur.fetchall()

            if not rows:
                raise RelationException(f"Table {table.upper()} is empty, fill it first")

            rel = []
            colored_print(f"Select {field}:", fore=Fore.GREEN)
            for row in rows:
                data = row_to_dict(cur, row)
                colored_print(f"\t{data['id']}: {data['name']}", fore=Fore.RED)
                rel.append(str(data['id']))
        return rel

    def create(self) -> dict:
        data = {}
        self.fields_info.pop('_id', None)
        for field, field_type in self.fields_info.items():
            try:
                if field.endswith('datetime'):
                    user_input = colored_input(f"Enter {field} [{DATETIME_FORMAT}]: ", back=Back.BLACK)
                    value = user_input and field_type.strptime(user_input, DATETIME_FORMAT)
                else:
                    while True:
                        rel = self.process_relation(field_type, field)
                        value = field_type(colored_input(f"Enter {field}: ", back=Back.BLACK))
                        if rel and value not in rel:
                            colored_print(
                                f"\nInvalid '{field}' with value: '{value}'",
                                fore=Fore.YELLOW
                            )
                            continue
                        break
            except ValueError:
                colored_print(f"Invalid input for {field}\nSet default value - None", fore=Fore.RED)
                value = None
            except RelationException as e:
                colored_print(str(e), back=Back.RED)
                sys.exit(1)

            data[field] = value
        return data


class SQLiteManager:
    def __init__(self, db_name: str = DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create(self, table_name: str):
        record = ModelManager(table_name).create()

        columns_str = ', '.join(record.keys())
        values_str = ', '.join(['?'] * len(record))

        self.cur.execute(
            f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})",
            tuple(record.values())
        )
        self.conn.commit()

    def get(self, table_name: str) -> list[tuple]:
        self.cur.execute(f"SELECT * FROM {table_name}")
        return self.cur.fetchall()

    def delete(self, table_name: str, _id: int) -> None:
        self.cur.execute(f"DELETE FROM {table_name} WHERE id = {_id}")
        self.conn.commit()

    def download(self) -> None:
        df = pd.read_sql_query(
            """
                SELECT c.number,
                       c.price,
                       c.start_datetime AS start,
                       c.end_datetime   AS end,
                       f.name           AS factory_name,
                       b.name           AS building_name,
                       r.name           AS repair_organization_name
                FROM contract c
                         JOIN building b ON c.building_id = b.id
                         JOIN factory f ON c.factory_id = f.id
                         JOIN repair_organization r ON c.repair_organization_id = r.id
                ORDER BY number
            """,
            self.conn
        )

        files_dir = os.path.join(PROJECT_DIR, 'output_files')
        file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        df.to_excel(f'{files_dir}/{file_name}.xlsx', index=False)

    def __del__(self) -> None:
        self.conn.close()
