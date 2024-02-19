FROM python:3.11.4-slim-bullseye
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update

RUN pip install --upgrade pip

# install project dependencies
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

COPY /scripts/start.sh /start.sh
RUN sed -i 's/\r$//' /start.sh && \
    chmod +x /start.sh

ENTRYPOINT ["sh", "-c", "/start.sh"]
