FROM python:3.11.6-slim
RUN apt-get update && apt-get -y install libffi-dev wget unzip

ENV DEPLOY_PATH=/var/www/manwha-reader
RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH

# install chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

# install chromedriver
ENV CHROMEDRIVER_VERSION=139.0.7258.66
RUN wget https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
  && unzip chromedriver-linux64.zip \
  && rm -rf chromedriver-linux64.zip \
  && mv ./chromedriver-linux64/chromedriver $DEPLOY_PATH/chromedriver \
  && rm -rf chromedriver-linux64/ \
  && chmod +x $DEPLOY_PATH/chromedriver

COPY pyproject.toml $DEPLOY_PATH/pyproject.toml
COPY poetry.lock $DEPLOY_PATH/poetry.lock

RUN pip install -U pip && pip install -U setuptools && pip install poetry
RUN poetry install --no-interaction --without dev

COPY . $DEPLOY_PATH/.

EXPOSE 8000
