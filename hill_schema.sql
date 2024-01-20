CREATE TABLE IF NOT EXISTS hill (
    record_datetime DATETIME PRIMARY KEY,
    active BOOLEAN,
    total_count SMALLINT(5),
    total_percent FLOAT,
    east_count SMALLINT(5),
    east_percent FLOAT,
    tower_count SMALLINT(5),
    tower_percent FLOAT,
    west_count SMALLINT(5),
    west_percent FLOAT
)