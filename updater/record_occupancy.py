import requests
import datetime
from typing import Dict, Any, List
import logging
import os
from dataclasses import dataclass


HILL_API_URL = "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=264&library=hill"

HUNT_API_URL = "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=1356&library=hunt"


@dataclass
class HillRecord:
    record_datetime: datetime.datetime
    active: bool
    total_count: int
    total_percent: float
    east_count: int
    east_percent: float
    tower_count: int
    tower_percent: float
    west_count: int
    west_percent: float

    def to_json(self) -> dict:
        return {
            "record_datetime": self.record_datetime.isoformat(" ", "seconds").split("+")[0],
            "active": self.active,
            "total_count": self.total_count,
            "total_percent": self.total_percent,
            "east_count": self.east_count,
            "east_percent": self.east_percent,
            "tower_count": self.tower_count,
            "tower_percent": self.tower_percent,
            "west_count": self.west_count,
            "west_percent": self.west_percent
        }


@dataclass
class HuntRecord:
    record_datetime: datetime.datetime
    active: bool
    total_count: int
    total_percent: float
    level2_count: int
    level2_percent: float
    level3_count: int
    level3_percent: float
    level4_count: int
    level4_percent: float
    level5_count: int
    level5_percent: float

    def to_json(self) -> dict:
        return {
            "record_datetime": self.record_datetime.isoformat(" ", "seconds").split("+")[0],
            "active": self.active,
            "total_count": self.total_count,
            "total_percent": self.total_percent,
            "level2_count": self.level2_count,
            "level2_percent": self.level2_percent,
            "level3_count": self.level3_count,
            "level3_percent": self.level3_percent,
            "level4_count": self.level4_count,
            "level4_percent": self.level4_percent,
            "level5_count": self.level5_count,
            "level5_percent": self.level5_percent
        }


class DataStoreInterface:
    def insert_hill_record(self, record: HillRecord):
        return

    def insert_hunt_record(self, record: HuntRecord):
        return


class BusynessAPI(DataStoreInterface):
    def __init__(self, api_host: str, api_port: str):
        self.api_base_url = f"http://{api_host}:{api_port}"

    def insert_hill_record(self, record: HillRecord):
        url = self.api_base_url + "/api/hill"
        body = record.to_json()
        res = requests.post(url=url, json=body)
        if res.status_code != 200:
            raise Exception(res.json())

    def insert_hunt_record(self, record: HuntRecord):
        url = self.api_base_url + "/api/hunt"
        body = record.to_json()
        res = requests.post(url=url, json=body)
        if res.status_code != 200:
            raise Exception(res.json())


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


def log_hill_data(db: DataStoreInterface, current_datetime: datetime.datetime):
    api_data = get_api_data(HILL_API_URL)

    if api_data["isActive"]:

        areas = api_data["childCounts"]
        east_data = get_area_by_name(areas, "East")
        tower_data = get_area_by_name(areas, "Tower")
        west_data = get_area_by_name(areas, "West")

        try:
            new_record = HillRecord(
                current_datetime,
                True,
                api_data["count"],
                api_data["percentage"],
                east_data["count"],
                east_data["percentage"],
                tower_data["count"],
                tower_data["percentage"],
                west_data["count"],
                west_data["percentage"]
            )
        except KeyError as e:
            raise Exception(f"error parsing API data: {e}")

        db.insert_hill_record(new_record)
    else:
        new_record = HillRecord(
            current_datetime,
            False,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )
        db.insert_hill_record(new_record)


def log_hunt_data(db: DataStoreInterface, current_datetime: datetime.datetime):
    api_data = get_api_data(HUNT_API_URL)

    if api_data["isActive"]:

        areas = api_data["childCounts"]
        l2_data = get_area_by_name(areas, "Level 2")
        l3_data = get_area_by_name(areas, "Level 3")
        l4_data = get_area_by_name(areas, "Level 4")
        l5_data = get_area_by_name(areas, "Level 5")

        try:
            new_record = HuntRecord(
                current_datetime,
                True,
                api_data["count"],
                api_data["percentage"],
                l2_data["count"],
                l2_data["percentage"],
                l3_data["count"],
                l3_data["percentage"],
                l4_data["count"],
                l4_data["percentage"],
                l5_data["count"],
                l5_data["percentage"]
            )
        except KeyError as e:
            raise Exception(f"error parsing API data: {e}")

        db.insert_hunt_record(new_record)
    else:
        new_record = HuntRecord(
            current_datetime,
            False,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None
        )
        db.insert_hunt_record(new_record)


def main():
    api_host = os.getenv("API_HOST")
    if api_host is None:
        raise Exception("API_HOST is not set")

    api_port = os.getenv("API_PORT")
    if api_port is None:
        raise Exception("API_PORT is not set")

    current_datetime = datetime.datetime.now(datetime.timezone.utc)

    api = BusynessAPI(api_host, api_port)

    try:
        log_hill_data(api, current_datetime)
        log_hunt_data(api, current_datetime)
    except Exception as e:
        logging.error(f"error while getting and saving data: {e}")
        print("Error:", e)
    else:
        logging.info("library busyness logging process completed")


if __name__ == "__main__":
    main()
