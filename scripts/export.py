import datetime
from db import initialize_db
from typing import Any


def export(records: list[Any], headers: list[str], filename: str):
    with open(f"data/export/{filename}", "w") as f:
        f.write(",".join(headers) + "\n")
        for record in records:
            record = list(record)
            record[0] = record[0].isoformat(" ", "seconds")
            record = ",".join(str(col) for col in record)
            f.write(f"{record}" + "\n")


if __name__ == "__main__":
    current_datetime = datetime.datetime.now()
    current_datetime_str = current_datetime.isoformat(
        "T", "seconds")

    connection = initialize_db()

    hill_records = connection.get_hill_records()

    hunt_records = connection.get_hunt_records()

    connection.close()

    export(hill_records, ["record_datetime", "active", "total_count", "total_percent", "east_count",
           "east_percent", "tower_count", "tower_percent", "west_count", "west_percent"], f"hill-{current_datetime_str}.csv")

    export(hunt_records, ["record_datetime", "active", "total_count", "total_percent", "level2_count", "level2_percent",
           "level3_count", "level3_percent", "level4_count", "level4_percent", "level5_count", "level5_percent"], f"hunt-{current_datetime_str}.csv")
