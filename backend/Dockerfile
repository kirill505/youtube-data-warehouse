FROM tiangolo/uvicorn-gunicorn:python3.10

COPY ./backend .
COPY ./pyproject.toml ./poetry.lock /backend/

WORKDIR /backend

RUN pip install --upgrade pip

RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]