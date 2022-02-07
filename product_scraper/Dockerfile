FROM mcr.microsoft.com/playwright:focal

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . ./product_scraper
CMD [ "python", "-m", "product_scraper" ]
