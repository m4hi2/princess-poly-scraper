from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    price: float
    full_price: float
    size: str
    color: str
    image_links: list
    description: str
    stock: int
