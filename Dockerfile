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

# Default config file
COPY config /opt/api-app/etc

# Docker-Entrypoint
COPY docker-entrypoint.sh /
RUN chmod 755 /docker-entrypoint.sh

# Application User
RUN useradd -ms /bin/bash appuser
USER appuser

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["python", "/opt/api-app/source/run.py"]
