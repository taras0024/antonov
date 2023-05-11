import sqlite3

from constants import DB_NAME


class InitDB:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    def create_factory(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS factory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT 
        )
        ''')
        self.conn.commit()

    def create_building(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS building (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT ,
            factory_id INTEGER ,

            FOREIGN KEY(factory_id) REFERENCES factory(id)
        )
        ''')
        self.conn.commit()

    def create_repair_organization(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS repair_organization (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT 
        )
        ''')
        self.conn.commit()

    def create_contract(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS contract (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER ,
            factory_id INTEGER ,
            building_id INTEGER ,
            repair_organization_id INTEGER ,
            price REAL ,
            start_datetime DATETIME,
            end_datetime DATETIME,

            FOREIGN KEY(factory_id) REFERENCES factory(id),
            FOREIGN KEY(building_id) REFERENCES building(id),
            FOREIGN KEY(repair_organization_id) REFERENCES repair_organization(id)
        )
        ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def __call__(self):
        self.create_factory()
        self.create_building()
        self.create_repair_organization()
        self.create_contract()
