# pull official base image
FROM python:3.8.6-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# lint
RUN pip install --upgrade pip setuptools && pip install flake8 && flake8 --ignore=E121,E501,F401,W605 .

# pull official base image
FROM python:3.8.6-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/uscis_service
RUN mkdir $APP_HOME
COPY . $APP_HOME
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && \
    apt-get install --reinstall -y build-essential && \
    apt-get install -y --no-install-recommends \
        gcc gfortran \
        libffi-dev \
        libjpeg-dev \
        musl-dev \
        netcat \
        python3 python3-dev \
        zlib1g-dev

RUN pip install --upgrade pip && \
        pip install -r requirements.txt

RUN chown -R app:app $APP_HOME
USER app
