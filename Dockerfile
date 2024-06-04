ARG PYTHON_VERSION=3.10-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

RUN apt-get update && apt-get install -y wget

COPY ./requirements.txt /code

RUN pip install -r ./requirements.txt

COPY . /code

EXPOSE 8000

WORKDIR /code/kakeibo

RUN chmod +x ./start.sh
CMD ["/bin/bash", "./start.sh"]