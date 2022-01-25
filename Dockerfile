FROM python:3.8-alpine3.14

RUN apk update
RUN pip install --no-cache-dir -U pip
RUN apk add --virtual .build-deps gcc musl-dev libffi-dev libpq
RUN apk add build-base
RUN apk add --no-cache mariadb-dev

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt


RUN apk del .build-deps
RUN apk del py-pip
RUN rm -rf /.cache/pip


COPY ./webapp/ /usr/DocumentLibrary/webapp/
WORKDIR /usr/DocumentLibrary/webapp/

EXPOSE 9876
