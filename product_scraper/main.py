from playwright.sync_api import sync_playwright

import bus
from products import Product

###################################################
#                  Queue settings                 #
###################################################
consume_queue = "product_links"
publish_queue = "products"

bus.declare([
    consume_queue,
    publish_queue,
])

###################################################
# Product page selectors for required information #
###################################################
product_name_selector = ".product__title"
color_selector = ".product__active-color-value"
size_selector = ".product__select--size>option"
current_price_selector = "span[data-product-price]"
original_price_selector = "s[data-compare-price]"
images_selector = ".product__zoom"
prodcut_description_selector = ".product-details__content-inner"

##################################################
# Starting Playwright instance                   #
##################################################
p = sync_playwright().start()
browser = p.chromium.launch()

def scrape(browser, link: str) -> None:
    """Given a link and browser instance scrapes product data and publishes
    serialized product objects to the queue

    Args:
        browser (Browser): Playwright Browser Instance
        link (str): Link of product
    """
    with browser.new_page() as page:

        page.goto(link)
        color = page.query_selector(color_selector).inner_text().lower()
        product_name = page.query_selector(product_name_selector).inner_text().lower().replace(color, "").strip()
        product_description = page.query_selector(prodcut_description_selector).inner_text().strip()
        current_price =  page.query_selector(current_price_selector).inner_text().replace("$", "")
        current_price = float(current_price)
        original_price = page.query_selector(original_price_selector).inner_text().replace("$", "")
        original_price = float(original_price)

        # Not rechecking for price in product sizes because price is fully hydrated and
        # has no fetch action when different sizes are selected.
        if original_price == "":
            original_price = current_price

        size_options_elements = page.query_selector_all(size_selector)
        size_stock_data = {s.get_attribute("value"): s.get_attribute("data-stock") for s in size_options_elements if s.get_attribute("data-stock")}

        images = page.query_selector_all(images_selector)
        image_links = set(["https:" + i.get_attribute("data-product-detail-zoom") for i in images])
        
        for size, stock in size_stock_data.items():
            product = Product(product_name, current_price, original_price, size, color, image_links, product_description, stock)
            bus.publish(publish_queue, str(product), pickleit=False)


def callback(ch, method, properties, message):
    try:
        scrape(browser, message.link)
        print(message.link)
    except Exception as e:
        print(e)
        print(message.link)

##################################################
#  Start Processing Data from the queue          #
##################################################
bus.consume(consume_queue, callback)
bus.loop()