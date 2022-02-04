from playwright.sync_api import sync_playwright

import bus
from products import Product

consume_queue = "product_links"
publish_queue = "products"
secondary_publish = "prod_name_for_debug"

bus.declare([
    consume_queue,
    publish_queue,
    secondary_publish
])


p = sync_playwright().start()
browser = p.chromium.launch()

def scrape(browser, link):
    with browser.new_page() as page:

        page.goto(link)
        color = page.query_selector(".product__active-color-value").inner_text().lower()
        product_name = page.query_selector(".product__title").inner_text().lower().replace(color, "").strip()
        variants_options_elements = page.query_selector_all(".product__select--size>option")
        current_price =  page.query_selector("span[data-product-price]").inner_text().replace("$", "")
        original_price = page.query_selector("s[data-compare-price]").inner_text().replace("$", "")

        if original_price == "":
            original_price = current_price

        variants_data = {v.get_attribute("value"): v.get_attribute("data-stock") for v in variants_options_elements if v.get_attribute("data-stock")}
        images = page.query_selector_all(".product__zoom")

        image_links = set(["https:" + i.get_attribute("data-product-detail-zoom") for i in images])
        product_description = page.query_selector(".product-details__content-inner").inner_text().strip()
        # print(product_name)
        # print(variants_data)
        
        product = Product(product_name, current_price, original_price, "", color, image_links, product_description, 0)
        bus.publish(secondary_publish, str(product), pickleit=False)
        for size, stock in variants_data.items():
            # print(size, stock)
            product = Product(product_name, current_price, original_price, size, color, image_links, product_description, stock)
            # print(product)
            bus.publish(publish_queue, str(product), pickleit=False)


def callback(ch, method, properties, message):
    try:
        scrape(browser, message.link)
        print(message.link)
    except Exception as e:
        print(e)
        print(message.link)

bus.consume(consume_queue, callback)
bus.loop()