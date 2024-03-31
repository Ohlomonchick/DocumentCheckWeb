FROM python:3.11-slim-bullseye
LABEL authors="Dmitry"

RUN apt-get update -y
RUN apt-get install -y pkg-config libicu-dev

RUN mkdir ./app
COPY ./requirements.txt ./app
COPY . ./app

WORKDIR /app

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations --noinput
RUN python manage.py migrate --noinput

EXPOSE 8000

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]