library(rmarkdown)
library(dotenv)
library(DBI)
library(RMySQL)

# file paths are prepended with frontend because this file
# should be run from the root directory of the project
source("frontend/helpers.R")

db <- dbConnect(RMySQL::MySQL(),
  dbname = "busyness",
  host = Sys.getenv("DB_HOST"),
  user = Sys.getenv("DB_USER"),
  password = Sys.getenv("DB_PASSWORD")
)

hill_data <- dbReadTable(db, "hill")
hill_data <- entries_since_n_hrs_ago(
  hill_data, to_datetime(hill_data$record_datetime), 24 * 7 * 5
)

hunt_data <- dbReadTable(db, "hunt")
hunt_data <- entries_since_n_hrs_ago(
  hunt_data, to_datetime(hunt_data$record_datetime), 24 * 7 * 5
)

dbDisconnect(db)

rmarkdown::render(
  "frontend/libraries.Rmd", "html_document",
  params = list(hill_data = hill_data, hunt_data = hunt_data)
)
