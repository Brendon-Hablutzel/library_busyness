import mysql.connector
import os
from typing import Sequence, Any


class BusynessDB:
    def __init__(self, user: str, password: str, host: str, database_name: str):
        connection = mysql.connector.MySQLConnection(
            user=user,
            password=password,
            host=host,
            database=database_name
        )

        self.connection = connection
        self.cursor = connection.cursor()

    def get_hill_records(self):
        self.cursor.execute(
            "SELECT * FROM hill ORDER BY record_datetime ASC")
        return self.cursor.fetchall()

    def get_hunt_records(self):
        self.cursor.execute(
            "SELECT * FROM hunt ORDER BY record_datetime ASC")
        return self.cursor.fetchall()

    def insert_hill_record(self, record: Sequence[Any]):
        self.cursor.execute(
            "INSERT INTO hill (record_datetime, active, total_count, total_percent, east_count, east_percent, tower_count, tower_percent, west_count, west_percent) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", record
        )
        self.connection.commit()

    def insert_hunt_record(self, record: Sequence[Any]):
        self.cursor.execute(
            "INSERT INTO hunt (record_datetime, active, total_count, total_percent, level2_count, level2_percent, level3_count, level3_percent, level4_count, level4_percent, level5_count, level5_percent) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", record
        )
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def initialize_db() -> BusynessDB:
    user = os.getenv("MYSQL_USER")
    if user is None:
        raise Exception("environment variable MYSQL_USER not set")

    password = os.getenv("MYSQL_PASSWORD")
    if password is None:
        raise Exception("environment variable MYSQL_PASSWORD not set")

    host = os.getenv("MYSQL_HOST")
    if host is None:
        raise Exception("environment variable MYSQL_HOST not set")

    database_name = os.getenv("MYSQL_DATABASE")
    if database_name is None:
        raise Exception("environment variable MYSQL_DATABASE not set")

    data_store = BusynessDB(
        user,
        password,
        host,
        database_name
    )

    return data_store
