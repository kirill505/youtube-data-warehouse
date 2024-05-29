FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt data pipeline src sql ./
RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]