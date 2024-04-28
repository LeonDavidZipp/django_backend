FROM python:3.9-bookworm
LABEL maintainer="lzipp"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

RUN python -m venv /py
RUN /py/bin/pip install --upgrade pip
RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get install -y build-essential libpq-dev
RUN /py/bin/pip install -r /tmp/requirements.txt
RUN rm -rf /tmp

ENV PATH="/py/bin:$PATH"
