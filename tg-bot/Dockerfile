FROM python:3.9.17-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /tg-bot

COPY . .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
