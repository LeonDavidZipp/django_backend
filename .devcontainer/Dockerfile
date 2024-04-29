FROM ubuntu:latest
LABEL maintainer="lzipp"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y curl && \
	apt-get update && apt-get install -y zsh && chsh -s /bin/zsh &&\
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
# Uses "Spaceship" theme with some customization. Uses some bundled plugins and installs some more from github
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.5/zsh-in-docker.sh)" -- \
    -t https://github.com/denysdovhan/spaceship-prompt \
    -a 'SPACESHIP_PROMPT_ADD_NEWLINE="false"' \
    -a 'SPACESHIP_PROMPT_SEPARATE_LINE="false"' \
    -p git \
    -p ssh-agent \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions

ENV PATH="/py/bin:$PATH"

