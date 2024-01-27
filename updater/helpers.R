to_datetime <- function(datetime_string) {
  return(as.POSIXct(datetime_string, tz = "", format = "%Y-%m-%d %H:%M:%OS"))
}

entries_since_n_hrs_ago <- function(entries, datetimes, hours) {
  most_recent_datetime <- tail(datetimes, n = 1)
  n_hrs_ago <- most_recent_datetime - 60 * 60 * hours
  entries_since <- subset(entries, datetimes >= n_hrs_ago)
  return(entries_since)
}
