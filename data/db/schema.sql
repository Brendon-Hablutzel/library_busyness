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
);

CREATE TABLE IF NOT EXISTS hunt (
    record_datetime DATETIME PRIMARY KEY,
    active BOOLEAN,
    total_count SMALLINT(5),
    total_percent FLOAT,
    level2_count SMALLINT(5),
    level2_percent FLOAT,
    level3_count SMALLINT(5),
    level3_percent FLOAT,
    level4_count SMALLINT(5),
    level4_percent FLOAT,
    level5_count SMALLINT(5),
    level5_percent FLOAT
);