FROM ubuntu:22.04

RUN apt-get update && apt-get install -y libmysqlclient-dev python3.10 python3-pip

WORKDIR /scripts

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["sh", "start.sh"]