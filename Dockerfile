FROM python:3.9-alpine3.16

RUN adduser --disabled-password service-user

COPY --chown=service-user:service-user requirements.txt /temp/requirements.txt
COPY --chown=service-user:service-user app /app

WORKDIR /app
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

USER service-user