from playwright.sync_api import sync_playwright

p = sync_playwright().start()
browser = p.chromium.launch(headless=False)
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


print(color)
print(product_name)
print(variants_data)
print(current_price)
print(original_price)