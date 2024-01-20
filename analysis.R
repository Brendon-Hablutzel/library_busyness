library(dotenv)
library(DBI)
library(RMySQL)

db <- dbConnect(RMySQL::MySQL(),
  dbname = "busyness",
  host = Sys.getenv("DB_HOST"),
  user = Sys.getenv("DB_USER"),
  password = Sys.getenv("DB_PASSWORD")
)

hill_data <- dbReadTable(db, "hill")
hunt_data <- dbReadTable(db, "hunt")

dbDisconnect(db)

to_datetime <- function(datetime_string) {
  return(as.POSIXct(datetime_string, tz = "", format = "%Y-%m-%d %H:%M:%S"))
}

# allow legend to be placed outside graph
par(xpd = TRUE)

# hunt
plot(
  to_datetime(hunt_data$record_datetime), hunt_data$total_count,
  xlab = "Datetime",
  ylab = "Occupancy (number of people)",
  type = "p", col = "blue", ylim = c(0, 1200)
)
lines(
  to_datetime(hunt_data$record_datetime), hunt_data$total_count,
  col = "blue"
)

# hill
points(
  to_datetime(hill_data$record_datetime), hill_data$total_count,
  col = "red"
)
lines(
  to_datetime(hill_data$record_datetime), hill_data$total_count,
  col = "red"
)

legend(
  "topleft",
  inset = c(0, -0.15), legend = c("Hill", "Hunt"),
  fill = c("red", "blue")
)
