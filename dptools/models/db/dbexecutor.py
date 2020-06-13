"""
dbexecutor.py

Module for DBExecutor class object

Copyright (C) 2018 Disappeer Labs
License: GPLv3
"""

import sqlite3


class DBExecutor:

    def __init__(self, db_file_path):
        self.database = db_file_path

    def execute(self, *args):
        connection, cursor = self._connection_cursor(*args)
        self._commit_and_close(connection)

    def fetch_all(self, *args):
        connection, cursor = self._connection_cursor(*args)
        result = cursor.fetchall()
        self._commit_and_close(connection)
        return result

    def fetch_one(self, *args):
        connection, cursor = self._connection_cursor(*args)
        result = cursor.fetchone()
        self._commit_and_close(connection)
        return result

    def _connection_cursor(self, *args):
        connection = sqlite3.connect(self.database)
        cursor = connection.cursor()
        cursor.execute(*args)
        return connection, cursor

    def _commit_and_close(self, connection):
        connection.commit()
        connection.close()
