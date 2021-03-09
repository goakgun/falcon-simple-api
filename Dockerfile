FROM python:3.8-slim

USER root

ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux

RUN mkdir /opt/api-app # app workdir
RUN mkdir /opt/api-app/etc # config file location

WORKDIR /opt/api-app

COPY requirements.txt /opt/api-app/requirements.txt

RUN pip install -r /opt/api-app/requirements.txt

COPY source /opt/api-app/source

# Uncomment on test environment / single instance
# COPY config /opt/api-app/etc

ENTRYPOINT ["python", "/opt/api-app/source/run.py"]
