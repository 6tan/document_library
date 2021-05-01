FROM python:3.7-alpine3.11

RUN apk update
RUN pip install --no-cache-dir -U pip
RUN apk add --virtual .build-deps gcc musl-dev libffi-dev libpq
RUN apk add postgresql-dev
RUN apk add build-base
RUN apk add --no-cache mariadb-dev

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


RUN apk del .build-deps
RUN apk del py-pip
RUN rm -rf /.cache/pip


COPY ./webapp/ /usr/sample-api/webapp/
WORKDIR /usr/sample-api/webapp/

EXPOSE 9876
