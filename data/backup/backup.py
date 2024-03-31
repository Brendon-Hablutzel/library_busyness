import requests
import datetime
import csv
import os


def backup_hill_data(api_host, api_port):
    current_datetime = datetime.datetime.now().isoformat(timespec="seconds")

    res = requests.get(f"http://{api_host}:{api_port}/api/hill")
    data = res.json()

    if not data['success']:
        raise Exception(f"Failed to fetch data from the database via API")

    data = data['result']

    with open(f"./export/hill-{current_datetime}.csv", "w+") as f:
        f.write("record_datetime,active,total_count,total_percent,east_count,east_percent,tower_count,tower_percent,west_count,west_percent\n")

        for record in data:
            f.write(f"{record['record_datetime']},{record['active']},{record['total_count']},{record['total_percent']},{record['east_count']},{record['east_percent']},{record['tower_count']},{record['tower_percent']},{record['west_count']},{record['west_percent']}\n")


def backup_hunt_data(api_host, api_port):
    current_datetime = datetime.datetime.now().isoformat(timespec="seconds")

    res = requests.get(f"http://{api_host}:{api_port}/api/hunt")
    data = res.json()

    if not data['success']:
        raise Exception(f"Failed to fetch data from the database via API")

    data = data['result']

    with open(f"./export/hunt-{current_datetime}.csv", "w+") as f:
        f.write("record_datetime,active,total_count,total_percent,level2_count,level2_percent,level3_count,level3_percent,level4_count,level4_percent,level5_count,level5_percent\n")

        for record in data:
            f.write(f"{record['record_datetime']},{record['active']},{record['total_count']},{record['total_percent']},{record['level2_count']},{record['level2_percent']},{record['level3_count']},{record['level3_percent']},{record['level4_count']},{record['level4_percent']},{record['level5_count']},{record['level5_percent']}\n")


def main():
    api_host = os.getenv("API_HOST")
    if api_host is None:
        raise KeyError("API_HOST is not set")

    api_port = os.getenv("API_PORT")
    if api_port is None:
        raise KeyError("API_PORT is not set")

    backup_hill_data(api_host, api_port)
    backup_hunt_data(api_host, api_port)


if __name__ == "__main__":
    main()
