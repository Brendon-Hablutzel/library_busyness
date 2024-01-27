library(rmarkdown)
library(DBI)
library(RMySQL)

source("helpers.R")

db <- dbConnect(RMySQL::MySQL(),
  dbname = Sys.getenv("MYSQL_DATABASE"),
  host = Sys.getenv("MYSQL_HOST"),
  user = Sys.getenv("MYSQL_USER"),
  password = Sys.getenv("MYSQL_PASSWORD")
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
  "libraries.Rmd",
  "html_document",
  output_dir = "static",
  params = list(hill_data = hill_data, hunt_data = hunt_data)
)
