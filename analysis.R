hunt_data <- read.csv("hunt.csv")

hill_data <- read.csv("hill.csv")

to_datetime <- function(datetime_string) {
  return(as.POSIXct(datetime_string, tz = "", format = "%Y-%m-%d %H:%M:%OS"))
}

# allow legend to be placed outside graph
par(xpd = TRUE)

# hunt
plot(
  to_datetime(hunt_data$datetime), hunt_data$total.count,
  xlab = "Datetime",
  ylab = "Occupancy (number of people)",
  type = "p", col = "blue", ylim = c(0, 1000)
)
lines(
  to_datetime(hunt_data$datetime), hunt_data$total.count,
  col = "blue"
)

# hill
points(
  to_datetime(hill_data$datetime), hill_data$total.count,
  col = "red"
)
lines(
  to_datetime(hill_data$datetime), hill_data$total.count,
  col = "red"
)

legend(
  "topleft",
  inset = c(0, -0.15), legend = c("Hill", "Hunt"),
  fill = c("red", "blue")
)