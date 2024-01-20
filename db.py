import mysql.connector
from typing import Any, Sequence


class BusynessDB:
    def __init__(self, connection: mysql.connector.MySQLConnection):
        self.connection = connection
        self.cursor = connection.cursor()

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
