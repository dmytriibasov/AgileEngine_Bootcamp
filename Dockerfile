# syntax=docker/dockerfile:1
FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY apps .
COPY config .
COPY manage.py .
