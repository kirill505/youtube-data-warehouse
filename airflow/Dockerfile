FROM apache/airflow:2.9.2

COPY requirements.txt /requirements.txt

RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

USER root

RUN apt-get update && apt-get install -y wget

USER airflow