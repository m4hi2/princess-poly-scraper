FROM python:latest

WORKDIR /src

COPY requiremnts.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "main.py" ]
