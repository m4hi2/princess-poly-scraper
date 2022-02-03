import re

def find_product_links(xml_file: str) -> list:
    """Finds links related to products in the sitemap.xml file.

    Args:
        xml_file (str): The sitemap.xml file. From the response object.

    Returns:
        product_links (list): A list of product links.
    """
    # Didn't want to use BeautifulSoup, so I just used regex to find the links
    links = re.findall('<loc>(.*?)</loc>', xml_file)
    return [link for link in links if "products" in link]
