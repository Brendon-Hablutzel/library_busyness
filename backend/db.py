import mysql.connector
from typing import Any, Sequence


HILL_SCHEMA = "schemas/hill.sql"
HUNT_SCHEMA = "schemas/hunt.sql"
DATABASE_NAME = "busyness"


class BusynessDB:
    def __init__(self, user: str, password: str, host: str):
        connection = mysql.connector.MySQLConnection(
            user=user,
            password=password,
            host=host,
            database=DATABASE_NAME
        )

        self.connection = connection
        self.cursor = connection.cursor()

    def create_hill_table(self):
        with open(HILL_SCHEMA, "r") as f:
            schema = f.read()
            self.cursor.execute(schema)

    def create_hunt_table(self):
        with open(HUNT_SCHEMA, "r") as f:
            schema = f.read()
            self.cursor.execute(schema)

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
