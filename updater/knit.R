library(rmarkdown)
library(DBI)
library(RMySQL)

environment <- Sys.getenv("ENVIRONMENT")

if (environment == "development") {
  hill_data <- tail(read.csv("hill.csv", header = TRUE), n = 500)
  hunt_data <- tail(read.csv("hunt.csv", header = TRUE), n = 500)

  rmarkdown::render(
    "libraries.Rmd",
    "html_document",
    output_dir = "static",
    params = list(hill_data = hill_data, hunt_data = hunt_data)
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

  hunt_data <- dbGetQuery(
    db,
    "SELECT * FROM hunt ORDER BY record_datetime DESC LIMIT 500"
  )

  dbDisconnect(db)

  rmarkdown::render(
    "libraries.Rmd",
    "html_document",
    output_dir = "static",
    params = list(hill_data = hill_data, hunt_data = hunt_data)
  )
} else {
  write(paste("invalid environment: ", environment), stderr())
}
