import json

from DataDao.DataDao import DataDao
from pojo import ProductDetail


class JsonDataDaoImpl(DataDao):
    def __init__(self, file_url):
        self.file_url = file_url
        pass

    def readData(self):
        try:
            with open(self.file_url, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def writeData(self, productDetail: ProductDetail, product_id: str):
        data = self.readData()
        data.setdefault(product_id, []).append(json.dumps(productDetail.__dict__))
        with open(self.file_url, 'w') as file:
            json.dump(data, file, indent=4)


