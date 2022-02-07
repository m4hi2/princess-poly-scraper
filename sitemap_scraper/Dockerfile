# This docker image needs other packages and shouldn't be
# ran without the docker-compose.yml file provided.
FROM python:latest

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . ./app
CMD [ "python", "-m", "app" ]
