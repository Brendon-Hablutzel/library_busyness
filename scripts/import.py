import csv
from db import initialize_db

if __name__ == "__main__":
    connection = initialize_db()

    hill_import_file = "data/import/hill.csv"
    with open(hill_import_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            row = (
                row[0],
                bool(row[1]),
                int(row[2]),
                float(row[3]),
                int(row[4]),
                float(row[5]),
                int(row[6]),
                float(row[7]),
                int(row[8]),
                float(row[9])
            )
            connection.insert_hill_record(row)

    hunt_import_file = "data/import/hunt.csv"
    with open(hunt_import_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            row = (
                row[0],
                bool(row[1]),
                int(row[2]),
                float(row[3]),
                int(row[4]),
                float(row[5]),
                int(row[6]),
                float(row[7]),
                int(row[8]),
                float(row[9]),
                int(row[10]),
                float(row[11])
            )
            connection.insert_hunt_record(row)

    connection.close()
