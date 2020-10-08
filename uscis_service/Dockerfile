###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.1-slim-buster as builder

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
COPY . /usr/src/app/
RUN pip install --upgrade pip && pip install flake8 && \
    flake8 --ignore=E121,E501,F401,W605 .

#########
# FINAL #
#########

# pull official base image
FROM python:3.8.1-slim-buster

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/uscis_service
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install dependencies
COPY --from=builder /usr/src/app/requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    apt-get install libffi-dev && \
    pip install --upgrade pip
ENV BUILD_DEPS gcc g++
RUN apt-get update && \
    apt-get install -y $BUILD_DEPS --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt

COPY . $APP_HOME
# add cron jobs
COPY ./uscis-cron /etc/cron.d
RUN apt-get update && \
    apt-get -y install cron && \
    chmod 0644 /etc/cron.d/uscis-cron && \
    crontab /etc/cron.d/uscis-cron && \
    touch /var/log/cron.log

RUN chown -R app:app $APP_HOME
USER app

CMD ["cron", "-f"]
