FROM python:3.8-slim

LABEL maintainer="Andy Craze <accraze@gmail.com>"

COPY ./requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc libsndfile1

COPY ./src /src

CMD gunicorn --bind 0.0.0.0:$PORT src.app:app


