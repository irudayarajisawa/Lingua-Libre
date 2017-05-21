FROM python:2.7

RUN apt-get update \
  # for oggenc
  && apt-get install -y vorbis-tools \
  # for mysql
  && apt-get install -y python-pip python-dev libmysqlclient-dev

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
