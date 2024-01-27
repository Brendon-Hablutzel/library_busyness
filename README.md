# Library Busyness

An application that stores data about the busyness of NCSU's libraries and compiles it into an html summary using rmarkdown.

# Deployment with Docker

Required environment variables:
 - `MYSQL_ROOT_PASSWORD` - the password to set for the root user in the db container
 - `MYSQL_USER` - the user to use in the data logger when connecting to the database
 - `MYSQL_PASSWORD` - the password to use in the data logger when connecting to the database

Start nginx server: `docker compose up server -d`

Run updater and stop database afterward: `docker compose run updater && docker compose down db`

Stop all services: `docker compose down`
