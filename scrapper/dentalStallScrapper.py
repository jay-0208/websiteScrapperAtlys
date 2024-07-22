import time

import requests
from bs4 import BeautifulSoup
from DataDao.JsonDataDaoImpl import *

from pojo.ProductDetail import ProductDetail

global_retry_count = 3


def scrap_dentalStall(total_pages=0):
    curr_time = int(time.time())
    url = "https://dentalstall.com/shop/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    error_items = []
    if total_pages == 0:
        for item in soup.select("div.mf-shop-content li a.page-numbers"):
            item = item.text.strip()
            if item.isnumeric() and int(item) > total_pages:
                total_pages = int(item)

    success_processed = 0
    success_updated = 0
    failed_cnt = 0
    jsonDao = JsonDataDaoImpl("data.json")
    jsonData = jsonDao.readData()
    for page_no in range(1, total_pages + 1):

        retry_count = 0
        while retry_count < global_retry_count:
            try:
                url = f"https://dentalstall.com/shop/page/{page_no}/"
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                retry_count = 0
                break
            except Exception:
                time.sleep(5)
                retry_count += 1

        if retry_count == global_retry_count:
            continue

        for item in soup.select("div.mf-product-price-box"):
            retry_count = 0
            while retry_count < global_retry_count:
                try:
                    price = ""
                    try:
                        price = str(item.find("span", class_="woocommerce-Price-amount amount").text.strip()[1:])
                    except:
                        # item is out of stock
                        pass

                    product_details = item.find("div", class_="addtocart-buynow-btn")
                    product_name = product_details.find("a").get('aria-label', '').replace("Add to cart: “",
                                                                                           "").replace(
                        "”", "").replace("Select options for “", "")

                    image_link = product_details.find("a", class_="buy-now-btn button").get('href', '')

                    product_id = product_details.find("a").get('data-product_id', '')

                    product_details = ProductDetail(image_link, price, product_name)

                    current_product_details = jsonData.get(product_id)
                    if current_product_details is None or not compareProductDetails(current_product_details[0],
                                                                                    product_name, price, image_link):
                        jsonDao.writeData(product_details, product_id)
                        success_updated += 1

                    success_processed += 1
                    break
                except Exception:
                    error_items.append(item)
                    retry_count += 1
                    if retry_count == global_retry_count: failed_cnt += 1

    createSummary(success_processed, success_updated, failed_cnt, curr_time)
    return


def compareProductDetails(product_detail, product_name, product_price, image_href):
    if product_detail.get("name") == product_name and product_detail.get("") == image_href and product_detail.get(
            "") == product_price:
        return True
    return False


def createSummary(success, success_updated, failed, starting_time):
    print("Scrapping Completed !!")
    print("Successfully Scraped : ", success)
    print("Updated Successfully : ", success_updated)
    print("Failed events : ", failed)
    print("time taken in seconds : ", int(time.time()) - starting_time)
