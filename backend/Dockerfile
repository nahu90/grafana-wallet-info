FROM python:3.10.4-buster

RUN apt-get update && apt-get install -y gettext binutils libproj-dev gdal-bin locales
RUN pip install --upgrade pip

RUN sed -i '/es_ES.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES:es
ENV LC_ALL es_ES.UTF-8

ENV TZ=America/Argentina/Buenos_Aires
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /config
ADD requirements.txt /config/
ADD requirements-docker.txt /config/
RUN pip install -r /config/requirements.txt
RUN pip install -r /config/requirements-docker.txt
