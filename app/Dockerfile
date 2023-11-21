FROM python:3.10.2-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install netcat gcc \
    && apt-get clean \
    && pip install --upgrade pip \ 
    && pip install uvicorn 

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . . 

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]