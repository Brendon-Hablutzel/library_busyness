FROM python:3.10

WORKDIR /backup

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "backup.py"]