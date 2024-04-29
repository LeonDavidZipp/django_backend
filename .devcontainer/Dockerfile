FROM ubuntu:latest
LABEL maintainer="lzipp"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y curl && \
	apt-get update && apt-get install -y zsh && \
	curl -fsSL https://get.docker.com | sh && \
	curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose && \
	chmod +x /usr/local/bin/docker-compose && \
	apt-get update && apt-get install python3 -y && \
	apt install python3.12-venv -y && \
	apt-get install libpq-dev python3-dev -y && \
	python3 -m venv /py && \
	/py/bin/pip install --upgrade pip && \
	apt-get update && apt-get install -y postgresql-client && \
	apt-get install -y build-essential libpq-dev && \
	/py/bin/pip install -r /tmp/requirements.txt && \
	rm -rf /tmp

ENV PATH="/py/bin:$PATH"

