FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY kafka_consumer.py kafka_consumer.py

CMD ["python", "kafka_consumer.py"]
