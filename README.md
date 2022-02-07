# Zelf Assignment

## How to run?

### With Docker

``` bash
docker compose up -d --scale product_scraper=5
```

The above command will run all the micro services and necessary infrastructure automatically.

### How to see data

Sorry, I didn't have the time to build a web service to view the data, I initially planned on
building one. Currently, we can connect to the postgresql service running on the docker container
from the command line and see the data.

``` bash
psql -h localhost -p 5438 -d postgres -U postgres -W
```

Provide `postgres` as password, when prompted. Then we can use standard SQL queries to
see the available data.

``` sql
SELECT name, size, price, color, stock FROM product;
```

## Assignment Details

### Site to scrape

`https://us.princesspolly.com/`

### Specification

Example product link: `https://us.princesspolly.com/products/huxley-set?nosto=frontpage-nosto-3`

- All product variants
  - For the URL above, the product can come in five colors and seven sizes per
      color, for a total of 35 variants
  - For each variant, what is the
    - Current price
    - Full price (this may be the same as the current price)
    - Is the item available and in-stock?
    - URLs for photos
- The following information
  - Product name
  - Product description

## Research of the site

This section is dedicated to find out anomalies of products for reference:

- Sold out example: `https://us.princesspolly.com/products/charvi-mini-dress-forest-burgundy?variant=39519437619284`
- Price Discount example: `https://us.princesspolly.com/products/the-soho-heels-beige`
- There is a occasional banner that pops up whose selector is: `close-button cw-close`
- The price for all the sizes must be same because there is **no network activity** when different sizes are selected
- In all product list, different color variants of the same product is served. So it's not reliable to get the original
  product that way.
  - possible approaches:
    - if product `color name` exists in product name then subtract the color to get the base products
    - if product name doesn't contain `color name` then the product name will be the base product
