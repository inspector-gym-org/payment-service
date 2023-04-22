# syntax=docker/dockerfile:1

FROM python:3.11-slim-bullseye AS requirements-stage

WORKDIR /tmp

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock /tmp/
RUN poetry export --output requirements.txt --with=prod

FROM python:3.11-slim-bullseye

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD [ "gunicorn", \
    "--bind", "0.0.0.0:80", \
    "--access-logfile", "-", \
    "--workers", "4", \
    "--worker-class", "uvicorn.workers.UvicornH11Worker", \
    "payment_service.main:app" ]

COPY ./payment_service /code/payment_service
