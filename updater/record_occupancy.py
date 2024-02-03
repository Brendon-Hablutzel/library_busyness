import requests
import datetime
from typing import Dict, Any, List
import logging
import os
import mysql.connector
from typing import Any, Sequence


HILL_API_URL = "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=264&library=hill"

HUNT_API_URL = "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=1356&library=hunt"


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

    def last_hill_record(self):
        self.cursor.execute(
            "SELECT * FROM hill ORDER BY record_datetime DESC LIMIT 1")
        return self.cursor.fetchone()

    def last_hunt_record(self):
        self.cursor.execute(
            "SELECT * FROM hunt ORDER BY record_datetime DESC LIMIT 1")
        return self.cursor.fetchone()

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


def get_api_data(url: str) -> Dict[str, Any]:
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        raise e
    else:
        return data


def get_area_by_name(areas: List[Dict[str, Any]], name: str) -> Dict[str, Any]:
    for area in areas:
        if area["name"] == name:
            return area
    raise Exception(f"No area with name {name} found")


def log_hill_data(db: BusynessDB, current_datetime: str):
    api_data = get_api_data(HILL_API_URL)

    areas = api_data["childCounts"]
    east_data = get_area_by_name(areas, "East")
    tower_data = get_area_by_name(areas, "Tower")
    west_data = get_area_by_name(areas, "West")

    try:
        new_record = (
            current_datetime,
            bool(api_data["isActive"]),
            int(api_data["count"]),
            float(api_data["percentage"]),
            int(east_data["count"]),
            float(east_data["percentage"]),
            int(tower_data["count"]),
            float(tower_data["percentage"]),
            int(west_data["count"]),
            float(west_data["percentage"])
        )
    except Exception as e:
        raise Exception(f"error parsing API data: {e}")

    db.insert_hill_record(new_record)


def log_hunt_data(db: BusynessDB, current_datetime: str):
    api_data = get_api_data(HUNT_API_URL)

    areas = api_data["childCounts"]
    l2_data = get_area_by_name(areas, "Level 2")
    l3_data = get_area_by_name(areas, "Level 3")
    l4_data = get_area_by_name(areas, "Level 4")
    l5_data = get_area_by_name(areas, "Level 5")

    try:
        new_record = (
            current_datetime,
            bool(api_data["isActive"]),
            int(api_data["count"]),
            float(api_data["percentage"]),
            int(l2_data["count"]),
            float(l2_data["percentage"]),
            int(l3_data["count"]),
            float(l3_data["percentage"]),
            int(l4_data["count"]),
            float(l4_data["percentage"]),
            int(l5_data["count"]),
            float(l5_data["percentage"])
        )
    except Exception as e:
        raise Exception(f"error parsing API data: {e}")

    db.insert_hunt_record(new_record)


def main():
    current_datetime = datetime.datetime.now()
    current_datetime_str = current_datetime.isoformat(" ", "seconds")

    # user = os.getenv("MYSQL_USER")
    # if user is None:
    #     raise Exception("environment variable MYSQL_USER not set")

    # password = os.getenv("MYSQL_PASSWORD")
    # if password is None:
    #     raise Exception("environment variable MYSQL_PASSWORD not set")

    # host = os.getenv("MYSQL_HOST")
    # if host is None:
    #     raise Exception("environment variable MYSQL_HOST not set")

    # database_name = os.getenv("MYSQL_DATABASE")
    # if database_name is None:
    #     raise Exception("environment variable MYSQL_DATABASE not set")

    # connection = BusynessDB(
    #     user,
    #     password,
    #     host,
    #     database_name
    # )

    connection = initialize_db()

    try:
        log_hill_data(connection, current_datetime_str)
        log_hunt_data(connection, current_datetime_str)
    except Exception as e:
        print("Error", e)
        logging.error(f"error while getting and saving data: {e}")
    else:
        logging.info("library busyness logging process completed")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
