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
RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/app/
RUN flake8 --ignore=E121,E501,F401,W605 .

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
RUN apt-get update && apt-get install -y --no-install-recommends netcat
RUN apt-get install libffi-dev
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip
ENV BUILD_DEPS gcc g++
RUN apt-get update && apt-get install -y $BUILD_DEPS --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# add cron jobs
RUN apt-get update && apt-get -y install cron
COPY ./uscis-cron /etc/cron.d
RUN chmod 0644 /etc/cron.d/uscis-cron
RUN touch /var/log/cron.log
RUN touch /var/log/cron-lin2.log
RUN crontab /etc/cron.d/uscis-cron
CMD ["cron", "-f"]

# change to the app user
USER app
