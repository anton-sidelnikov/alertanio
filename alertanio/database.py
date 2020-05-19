import logging

import psycopg2

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


class DBHelper:
    """Postgre client wrapper"""

    def __init__(self, host, port, user, password, db='alerta'):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db = db

    def __connect__(self):
        """Open connection"""
        try:
            self.con = psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password)
            self.con.autocommit = True
            self.cur = self.con.cursor()
        except (Exception, psycopg2.Error) as error:
            raise error('Error while connecting to PostgreSQL')

    def __disconnect__(self):
        """Close connection"""
        if self.con:
            self.con.commit()
            self.cur.close()
            self.con.close()
        LOGGER.info(f'Connection to database closed')

    def check_database_exist(self):
        """Create database if not exist"""
        if not [item for item in self.get(table='pg_catalog.pg_database', columns='datname') if self.db in item]:
            try:
                self.query(f'CREATE DATABASE {self.db}')
                LOGGER.info(f'Database: {self.db} succesfully created')
                return False
            except (Exception, psycopg2.Error) as error:
                LOGGER.error('Error while processing SQL request')
        return True

    def get(self, table, columns, condition=None, custom_clause=None, limit=None):
        """Select data from table"""
        if condition:
            query = f'SELECT {columns} FROM {table} WHERE {condition};'
        elif custom_clause:
            query = f'SELECT {columns} FROM {table} {custom_clause};'
        else:
            query = f'SELECT {columns} FROM {table};'
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows[len(rows) - limit if limit else 0:]

    def write(self, table, columns, data):
        """Insert data to table"""
        query = f'INSERT INTO {table} ({columns}) VALUES ({data});'
        self.cur.execute(query)
        self.con.commit()

    def query(self, sql):
        """Custom query"""
        self.cur.execute(sql)
        self.con.commit()
