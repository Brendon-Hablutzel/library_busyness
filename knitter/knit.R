library(rmarkdown)
library(jsonlite)
library(httr2)

unset_env_vars <- FALSE

api_host <- Sys.getenv("API_HOST")

if (api_host == "") {
  warning("API_HOST is not set")
  unset_env_vars <- TRUE
}

api_port <- Sys.getenv("API_PORT")

if (api_port == "") {
  warning("API_PORT is not set")
  unset_env_vars <- TRUE
}

if (unset_env_vars) {
  quit(status = 1)
}

base_api_url <- paste(
  "http://",
  api_host,
  ":",
  api_port,
  "/api",
  sep = ""
)

hill_api_url <- paste(base_api_url, "/hill/recent/500", sep = "")
hill_req <- request(hill_api_url)

hill_data <- req_perform(hill_req) %>%
  resp_body_string() %>%
  fromJSON()

hunt_api_url <- paste(base_api_url, "/hunt/recent/500", sep = "")
hunt_req <- request(hunt_api_url)

hunt_data <- req_perform(hunt_req) %>%
  resp_body_string() %>%
  fromJSON()

rmarkdown::render(
  "libraries.Rmd",
  "html_document",
  output_dir = "static",
  params = list(
    hill_data = hill_data,
    hunt_data = hunt_data
  )
)
