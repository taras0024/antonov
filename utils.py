from sqlite3 import Cursor

from colorama import Style


def row_to_dict(cursor: Cursor, rows: tuple) -> dict:
    res = {}
    for idx, col in enumerate(cursor.description):
        res[col[0]] = rows[idx]
    return res


def colored_print(text: str, fore: str = '', back: str = '') -> None:
    print(f"{fore}{back}{text}{Style.RESET_ALL}")


def colored_input(text: str, fore: str = '', back: str = '') -> str:
    return input(f"{fore}{back}{text}{Style.RESET_ALL}")
