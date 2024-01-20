import requests
import datetime
import mysql.connector
from typing import Dict, Any, List
from dotenv import load_dotenv
import logging
import os
from db import BusynessDB

load_dotenv()

logging.basicConfig(filename=os.getenv("LOG_FILE"),
                    filemode='a',
                    format='%(name)s at %(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

HILL_API_URL = "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=264&library=hill"

HUNT_API_URL = "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=1356&library=hunt"

DATABASE_NAME = "busyness"


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
        raise Exception(f"Error parsing and coercing API data: {e}")

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
        raise Exception(f"Error parsing and coercing API data: {e}")

    db.insert_hunt_record(new_record)


def main():
    current_datetime = datetime.datetime.now().isoformat(" ", "seconds")

    connection = mysql.connector.MySQLConnection(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=DATABASE_NAME
    )

    connection = BusynessDB(connection)

    try:
        log_hill_data(connection, current_datetime)
        log_hunt_data(connection, current_datetime)
    except Exception as e:
        logging.error(f"Error while getting and saving data: {e}")
    else:
        logging.info("Library busyness logging process completed")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
