# Library Busyness

An application that stores data about the busyness of NCSU's libraries and compiles it into an html summary using rmarkdown.

# Deployment with Docker

Required environment variables:
 - `MYSQL_ROOT_PASSWORD` - the password to set for the root user in the db container
 - `MYSQL_USER` - the user to use in the data logger when connecting to the database
 - `MYSQL_PASSWORD` - the password to use in the data logger when connecting to the database

Other environment variables and their defaults:
 - `ENVIRONMENT=production` - "development" (uses local csv files for data) or "production" (uses mysql docker container)
 - `MYSQL_DATABASE=busyness` - the name of the database to save records to
 - `MYSQL_HOST=db` - the database hostname

Start nginx server: `docker compose up server -d`

Run updater and stop database afterward: `docker compose run --rm updater && docker compose down db`

Stop all services: `docker compose down`

Run a script: `docker compose run --rm scripts <script>` where scripts is one of:
 - `import.py` - imports data from csv files in the scripts/data/imports directory (csv files must be named `hill.csv` and `hunt.csv`)
 - `export.py` - exports data into a csv file per library in the scripts/data/exports directory

# Data storage

There are two options for data storage, MySQL and CSV files.

## MySQL

Setting the `ENVIRONMENT` environment variable to `production` will set the system to using MySQL. This is the default for running with docker.

The schemas for the tables can be found in [schema.sql](db/schema.sql)

## CSV

Setting the `ENVIRONMENT` environment variable to `development` will set the system to using CSV files.

An example CSV file is shown below for each library:

### Hill
```
record_datetime,active,total_count,total_percent,east_count,east_percent,tower_count,tower_percent,west_count,west_percent
2023-09-07 08:00:02,1,38,0.02,6,0.01,17,0.01,15,0.04
2023-09-07 08:30:03,1,66,0.03,12,0.02,31,0.02,23,0.07
2023-09-07 09:00:02,1,122,0.05,32,0.06,62,0.04,28,0.08
2024-02-07 16:01:48,0,,,,,,,,
```
Note the last row is an example of a row where the library is inactive

### Hunt
```
record_datetime,active,total_count,total_percent,level2_count,level2_percent,level3_count,level3_percent,level4_count,level4_percent,level5_count,level5_percent
2023-09-07 08:00:02,1,31,0.02,2,0,13,0.04,5,0.01,11,0.05
2023-09-07 08:30:02,1,38,0.03,3,0.01,15,0.04,11,0.02,9,0.04
2023-09-07 09:00:01,1,56,0.04,9,0.02,26,0.08,14,0.03,7,0.03
2024-02-07 16:01:48,1,760,0.51,190,0.46,232,0.67,249,0.5,89,0.37
```
