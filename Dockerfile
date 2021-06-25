FROM ubuntu:latest as base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \ 
    && apt-get install -y python3-pip python3-dev \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip 

RUN apt-get update -y \
    && apt-get install -y wget \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb

FROM base
EXPOSE 8000

COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR /home
COPY . /home

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "1000", "app.main:create_app()"]