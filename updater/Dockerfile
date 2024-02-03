FROM ubuntu:22.04

# installation of r-base asks for location
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y libmysqlclient-dev r-base pandoc python3.10 python3-pip

WORKDIR /updater

COPY . .

RUN pip3 install -r requirements.txt

RUN R -e "install.packages('renv', repos = c(CRAN = 'https://cloud.r-project.org'))"

RUN R -e "renv::restore()"

CMD ["sh", "update.sh"]