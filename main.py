import argparse
from collections import defaultdict

from colorama import init as colorama_init

from constants import DB_TABLES
from db import InitDB
from handlers import (
    create,
    delete,
    get,
    download
)


class CommandParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    subparsers.required = True

    def __init__(self):
        self.extra_args = defaultdict(list)

    def parce_create_command(self):
        parser_create = self.subparsers.add_parser(
            'create',
            help='Create new row in the database'
        )
        parser_create.add_argument(
            'table_name',
            type=str,
            choices=DB_TABLES,
            help='Get rows from the database'
        )
        parser_create.set_defaults(func=create)
        self.extra_args['create'].append('table_name')

    def parce_get_command(self):
        parser_get = self.subparsers.add_parser('get', help='Get rows from the database')
        parser_get.add_argument(
            'table_name',
            type=str,
            choices=DB_TABLES,
            help='Get rows from the database'
        )
        parser_get.set_defaults(func=get)
        self.extra_args['get'].append('table_name')

    def parce_delete_command(self):
        parser_delete = self.subparsers.add_parser(
            'delete',
            help='Delete row from the database'
        )
        parser_delete.add_argument(
            'table_name',
            type=str,
            choices=DB_TABLES,
            help='Table name to delete row from'
        )
        parser_delete.add_argument(
            '_id',
            type=int,
            help='ID of the row to be deleted'
        )
        parser_delete.set_defaults(func=delete)
        self.extra_args['delete'].extend(['table_name', '_id'])

    def parce_download_command(self):
        parser_download = self.subparsers.add_parser(
            'download',
            help='Download data from the table "contract" to .xlsx file'
        )
        parser_download.set_defaults(func=download)

    def parse_args(self):
        self.parce_create_command()
        self.parce_get_command()
        self.parce_delete_command()
        self.parce_download_command()
        return self.parser.parse_args()


if __name__ == '__main__':
    colorama_init()
    InitDB()()
    parser = CommandParser()
    args = parser.parse_args()

    params = [getattr(args, param) for param in parser.extra_args.get(args.command, [])]
    func = getattr(args, 'func', lambda *_, **__: print('Command not found'))
    func(*params)
