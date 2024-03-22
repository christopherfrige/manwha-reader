FROM python:3.11.6-alpine3.18
RUN apk update && apk add --nocache --update bash libxslt libxslt-dev libffi-dev linux-headers alpine-sdk build-base \
    curl-dev openssl-dev gcc

ENV DEPLOY_PATH=/var/www/manwha-reader
RUN mkdir -p $DEPLOY_PATH

WORKDIR $DEPLOY_PATH

COPY pyproject.toml $DEPLOY_PATH/pyproject.toml
COPY poetry.lock $DEPLOY_PATH/poetry.lock

RUN pip install -U pip && pip install -U setuptools && pip install poetry
RUN poetry install --no-interaction --without dev

COPY . $DEPLOY_PATH/.

EXPOSE 8000
