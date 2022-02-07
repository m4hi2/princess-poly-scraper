FROM mcr.microsoft.com/playwright:focal

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "main.py" ]
