library(rmarkdown)
library(DBI)
library(RMySQL)

environment <- Sys.getenv("ENVIRONMENT")

if (environment == "development") {
  # take the most recent 500
  hill_data <- tail(read.csv("hill.csv", header = TRUE), n = 500)
  # get the most recent and check for activity
  hill_active <- tail(hill_data, n = 1)$active
  # take only rows where the library is active
  hill_data <- subset(hill_data, active == 1)
  # order the data chronologically
  hill_data <- hill_data[order(hill_data$record_datetime, decreasing = TRUE), ]
  most_recent_hill_record <- head(hill_data, n = 1)

  hunt_data <- tail(read.csv("hunt.csv", header = TRUE), n = 500)
  hunt_active <- tail(hunt_data, 1)$active
  hunt_data <- subset(hunt_data, active == 1)
  hunt_data <- hunt_data[order(hunt_data$record_datetime, decreasing = TRUE), ]
  most_recent_hunt_record <- head(hunt_data, n = 1)

  rmarkdown::render(
    "libraries.Rmd",
    "html_document",
    output_dir = "static",
    params = list(
      hill_data = hill_data,
      hill_active = hill_active,
      most_recent_hill_record = most_recent_hill_record,
      hunt_data = hunt_data,
      hunt_active = hunt_active,
      most_recent_hunt_record = most_recent_hunt_record
    )
  )
} else if (environment == "production") {
  db <- dbConnect(RMySQL::MySQL(),
    dbname = Sys.getenv("MYSQL_DATABASE"),
    host = Sys.getenv("MYSQL_HOST"),
    user = Sys.getenv("MYSQL_USER"),
    password = Sys.getenv("MYSQL_PASSWORD")
  )

  hill_data <- dbGetQuery(
    db,
    "SELECT * FROM hill ORDER BY record_datetime DESC LIMIT 500"
  )
  hill_active <- head(hill_data, n = 1)$active
  hill_data <- subset(hill_data, active == 1)
  most_recent_hill_record <- head(hill_data, n = 1)

  hunt_data <- dbGetQuery(
    db,
    "SELECT * FROM hunt ORDER BY record_datetime DESC LIMIT 500"
  )
  hunt_active <- head(hunt_data, n = 1)$active
  hunt_data <- subset(hunt_data, active == 1)
  most_recent_hunt_record <- head(hunt_data, n = 1)

  dbDisconnect(db)

  rmarkdown::render(
    "libraries.Rmd",
    "html_document",
    output_dir = "static",
    params = list(
      hill_data = hill_data,
      hill_active = hill_active,
      most_recent_hill_record = most_recent_hill_record,
      hunt_data = hunt_data,
      hunt_active = hunt_active,
      most_recent_hunt_record = most_recent_hunt_record
    )
  )
} else {
  write(paste("invalid environment: ", environment), stderr())
}
