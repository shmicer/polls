# pull official base image
FROM python:3.9.6-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/local/requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./compose/local/django/entrypoint.sh .
RUN sed -i 's/\r$//g' ./compose/local/django/entrypoint.sh
RUN chmod +x ./compose/local/django/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["./compose/local/django/entrypoint.sh"]