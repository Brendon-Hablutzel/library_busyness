FROM python:3.10

WORKDIR /updater

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "record_occupancy.py"]