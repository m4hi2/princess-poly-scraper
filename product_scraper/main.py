from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    # ?currency=BDT because the page was refreshing and playwright was getting timmedout on the page
    page.goto("https://us.princesspolly.com/products/huxley-set-black?currency=BDT")
    color = page.query_selector(".product__active-color-value").inner_text().lower()
    product_name = page.query_selector(".product__title").inner_text().lower().replace(color, "").strip()
    variants_options_elements = page.query_selector_all("#SingleOptionSelector-0>option")
    current_price =  page.query_selector("span[data-product-price]").inner_text().replace("$", "")
    original_price = page.query_selector("s[data-compare-price]").inner_text().replace("$", "")

    if original_price == "":
        original_price = current_price

    variants_data = {v.get_attribute("value"): v.get_attribute("data-stock") for v in variants_options_elements if v.get_attribute("data-stock")}
    images = page.query_selector_all(".product__zoom")

    image_links = set(["https:" + i.get_attribute("data-product-detail-zoom") for i in images])


    print(color)
    print(product_name)
    print(variants_data)
    print(current_price)
    print(original_price)
    print(image_links)