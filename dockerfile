# Dockerfile, Image, Container
FROM python:3.10-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/ /code/app

EXPOSE 8080

CMD python /code/app/main.py
