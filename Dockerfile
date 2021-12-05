# pull official base image ALPINE
FROM python:3.8.3-alpine

# set work directory
WORKDIR /usr/src/app

# set enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# # install psycopg2 dependencies
RUN apk update \
	&& apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev \
	&& apk add jpeg-dev zlib-dev libjpeg \
	&& apk add postgresql-dev

# RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN apk del build-deps

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]