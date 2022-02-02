# Zelf Assignment

## Site to scrape

`https://us.princesspolly.com/`

## Specification

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
