import requests
import csv
import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(filename=os.getenv("DATA_FETCH_LOG_FILE"),
                    filemode='a',
                    format='%(name)s at %(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                )

base_hill_url = "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=264&library=hill"

base_hunt_url = "https://www.lib.ncsu.edu/space-occupancy/realtime-data.php?id=1356&library=hunt"

def fetch_api(library_base_url):
    try:
        res = requests.get(library_base_url)

        data = res.json()
    except Exception as e:
        err = f"Unable to process request: {e}"
        logging.warning(err)
        raise Exception(err)

    return data


def record_data(filename, json_data, date_time):
    with open(filename, "a") as f:
        csv_writer = csv.writer(f)

        try:
            # summing a multi-dimensional list with an empty list flattens the multi-dimensional one
            level_data = sum([
                [level["count"], level["percentage"]] for level in json_data["childCounts"]], [])

            csv_writer.writerow([date_time, json_data["isActive"],
                                json_data["count"], json_data["percentage"]] + level_data)
        except Exception as e:
            err = f"Error parsing data and writing it to csv: {e}"
            logging.warning(err)
            raise Exception(err)

    logging.info(f"Library occupancy data succesfully logged to {filename}")


if __name__ == "__main__":
    date_time = date_time = datetime.datetime.now().isoformat(" ", "seconds")

    hunt_data = fetch_api(base_hunt_url)
    record_data("hunt.csv", hunt_data, date_time)

    hill_data = fetch_api(base_hill_url)
    record_data("hill.csv", hill_data, date_time)
