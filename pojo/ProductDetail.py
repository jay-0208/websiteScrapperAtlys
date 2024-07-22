class ProductDetail:
    def __init__(self, image_href, price, name):
        self.name = name
        self.price = float(price)
        self.image_href = image_href
