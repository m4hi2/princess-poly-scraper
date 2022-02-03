import re
import uuid

import requests
import bus
from tasks import Task

def main():
    main_sitemap = "https://us.princesspolly.com/sitemap.xml"
    sitemap_response = requests.get(main_sitemap)
    product_sitemap_links = find_product_links(sitemap_response.text)
    for product_sitemap_link in product_sitemap_links:
        product_response = requests.get(product_sitemap_link)
        product_links = find_product_links(product_response.text)
        for product_link in product_links:
            task = Task(uuid.uuid4().hex, product_link)
            bus.publish(publish_queue, task, pickleit=True)

def find_product_links(xml_file: str) -> list:
    """Finds links related to products in the sitemap.xml file.

    Args:
        xml_file (str): The sitemap.xml file. From the response object.

    Returns:
        product_links (list): A list of product links.
    """
    # Didn't want to use BeautifulSoup, so I just used regex to find the links
    links = re.findall('<loc>(.*?)</loc>', xml_file)
    # Using list comprehension to filter out the links that aren't product links
    return [link for link in links if "products" in link]

if __name__ == "__main__":
    publish_queue = "product_links"
    bus.declare([publish_queue])
    main()
