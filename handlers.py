from constants import DB_NAME
from db.managers import SQLiteManager
from utils import row_to_dict


def create(table_name: str) -> None:
    SQLiteManager(DB_NAME).create(table_name)


def delete(table_name: str, _id: int) -> None:
    SQLiteManager(DB_NAME).delete(table_name, _id)


def get(table_name: str):
    sql_manager = SQLiteManager(DB_NAME)
    rows = sql_manager.get(table_name)
    for row in rows:
        data = row_to_dict(sql_manager.cur, row)
        print(data)


def download():
    SQLiteManager(DB_NAME).download()
