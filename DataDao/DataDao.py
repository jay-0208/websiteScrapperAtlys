from abc import abstractmethod

from pojo import ProductDetail


class DataDao():

    @abstractmethod
    def readData(self):
        pass

    @abstractmethod
    def writeData(self, productDetail: ProductDetail, product_id : str):
        pass
