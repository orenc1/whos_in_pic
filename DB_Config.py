import os

work_mode = None
DATABASE_NAME = 'whoinpic_db'


if 'DATABASE_URL' in os.environ:
    work_mode = 'Cloud'
    DATABASE_URL = os.environ['DATABASE_URL']
else:
    work_mode = 'Local'
    DATABASE_URL = '127.0.0.1'
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD = 'P@ssw0rd'
