# FROM ubuntu:20.04
FROM tiangolo/meinheld-gunicorn-flask:python3.8


LABEL version="0.1"
LABEL David Sean "https://github.com/davidsean"

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt upgrade -y && apt install -y git sudo locales && locale-gen en_US.UTF-8


# Grab dependencies and generate locale
WORKDIR /instance

# add package dependancy indices
COPY apt-packages.txt /instance/apt-packages.txt
COPY requirements.txt /instance/requirements.txt

RUN DEBIAN_FRONTEND=noninteractive TZ=America/New_York \
    xargs -a apt-packages.txt apt install \
    -y --no-install-recommends --fix-missing

RUN pip install -r requirements.txt

ADD ./app /instance/app
# ADD ./certs /instance/certs
