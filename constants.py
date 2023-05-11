import os

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DB_NAME = 'sqlite3.db'
DB_TABLES = (
    'factory',
    'building',
    'repair_organization',
    'contract',
)
PROJECT_DIR = os.path.dirname(__file__)
