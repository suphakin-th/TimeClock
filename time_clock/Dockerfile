FROM python:3.8.10-buster

# Environment variables
ARG API_KEY
ENV API_KEY=$API_KEY

RUN apt-get update
RUN apt-get install -y software-properties-common

RUN apt-get install -y \
    python3-pip python3-dev python3-setuptools \
    --no-install-recommends

RUN apt-get update && apt-get install gettext nano vim -y

RUN pip3 install --upgrade pip

WORKDIR /src
COPY . /src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN echo "Asia/Bangkok" > /etc/timezone && rm /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

CMD python3 manage.py runserver 0.0.0.0:8000