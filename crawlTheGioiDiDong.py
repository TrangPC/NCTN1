from selenium import webdriver
import time
import numpy as np
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException, ElementClickInterceptedException

driver = webdriver.Chrome(executable_path='D:\chromedriver')
driver.get('https://www.thegioididong.com/dtdd')

# Lặp cho đến khi hiện thị hết các điện thoại lên màn hình
loop = True
while loop:
    try:
        viewMore = driver.find_element(By.CLASS_NAME, 'view-more')
        view = viewMore.find_element(By.TAG_NAME, 'a')
        remain = viewMore.find_element(By.CLASS_NAME, 'remain').text
        if int(remain) > 20:
            view.click()
        else:
            view.click()
            loop = False

        # print(remain)

    except ElementClickInterceptedException:
        print('Don\'t load data')
        break
    except NoSuchElementException:
        print('Don\'t load data')
        break


listProducts = driver.find_element(By.CLASS_NAME, 'listproduct')

titles = listProducts.find_elements(By.TAG_NAME, 'h3')
productTitles = [title.text for title in titles]

imgsClass = listProducts.find_elements(By.CLASS_NAME, 'item-img_42')
productImages = []
for i in range(0, len(imgsClass)):
    try:
        img = imgsClass[i].find_element(By.CSS_SELECTOR,'img [alt]')
        productImages.append(img.get_attribute('src'))
    except NoSuchElementException:
        productImages.append("NULL")
        continue
    except NoSuchAttributeException:
        productImages.append("NULL")
try:
    productSizes = []
    for i in range(0, len(productTitles)):
        size = listProducts.find_element(By.CLASS_NAME,'__cate_42')
        sizes = size.find_element(By.CLASS_NAME,'gray-bg')
        productSizes.append(size.text)
except NoSuchElementException:
    productSizes.append("NULL")


links = listProducts.find_elements(By.CSS_SELECTOR,'li [data-name]')
productLinks = [link.get_attribute('href') for link in links]


productOldPrice,productPercent, productPrice, productSpecialPrice, productStorage = [], [], [], [], []

for i in range(0, len(productTitles)):
    try:
        price = links[i].find_element(By.TAG_NAME, 'strong')
        productPrice.append(price.text)
    except NoSuchElementException:
        productPrice.append("NULL")



for i in range(0, len(productTitles)):
    try:

        old_price = links[i].find_element(By.CLASS_NAME, 'price-old')
        productOldPrice.append(old_price.text)

        discount = links[i].find_element(By.CLASS_NAME, 'percent')
        productPercent.append(discount.text)

    except NoSuchElementException:
        productOldPrice.append('NULL')
        productPercent.append('NULL')
        continue

for i in range(0, len(productTitles)):
    try:
        storage = links[i].find_element(By.CLASS_NAME, 'prods-group')
        productStorage.append(storage.text)
    except NoSuchElementException:
        productStorage.append('NULL')

for i in range(0, len(productTitles)):
    try:
        specialPrice = links[i].find_element(By.CLASS_NAME, 'fightprice')
        productSpecialPrice.append(specialPrice.text)
    except NoSuchElementException:
        productSpecialPrice.append('NULL')

totalComments = []
for i in range(0, len(productTitles)):
    try:
        comments = links[i].find_element(By.CLASS_NAME, 'item-rating-total')
        totalComments.append(comments.text)
    except NoSuchElementException:
        totalComments.append('NULL')

# print(productTitles)
# print(len(productTitles))
# print(len(links))
# print(productLinks)
# print(productImages)
# print(len(productImages))
# print(len(productSizes))
# print(productSizes)
# print(len(productPrice))
# print(productPrice)
# print(len(productOldPrice))
# print(productOldPrice)
# print(len(productPercent))
# print(productPercent)
# print(len(productStorage))
# print(productStorage)
# print(len(productSpecialPrice))
# print(productSpecialPrice)
# print(len(totalComments))
# print(totalComments)

productView = pd.DataFrame(list(zip(productTitles, productImages, productLinks, productSizes,productStorage,productPrice,productPercent,productOldPrice,productSpecialPrice, totalComments)), columns=["Title","Image","URL","Size","Storage","Price","Discount","Old Price", "Special Price", "Total Comments"])
# productView.info()
# print(productView)

productColor, productRate, productConfiguration = [], [], []

for i in range(0, len(productTitles)):
#
    driver.get(productLinks[i])

    # dữ liệu thử nghiệm: sản phẩm đầu tiên
    # driver.get(productLinks[0])

    try:
        color = driver.find_element(By.CLASS_NAME, 'box03.color.group.desk').text
        productColor.append(color)
    except NoSuchElementException:
        productColor.append("NULL")
    point = driver.find_element(By.CLASS_NAME, 'point')
    rate = point.find_element(By.TAG_NAME, 'p').text
    productRate.append(rate)

    parameters = driver.find_element(By.CLASS_NAME, 'parameter')
    productConfiguration.append(parameters.text)

    # print(productColor)
    # print(productRate)
    # print(productConfiguration)

    detailProduct = pd.DataFrame(list(zip(productColor, productRate, productConfiguration)), columns= ["Color", "Rate", "Configuration"])
    # detailProduct.info()

    Product = pd.concat([productView, detailProduct], axis=1)
    # Product.info()
    # print(Product.head(1).T)
#
#     # Lấy các comment về sản phẩm
    cmtProduct = []
    try:
        more = driver.find_element(By.CLASS_NAME, 'box-flex')
        cmtLink = more.find_element(By.TAG_NAME, 'a')
        cmtLink.click()

        listComments = driver.find_element(By.CLASS_NAME, "comment-list")

        names = listComments.find_elements(By.CLASS_NAME, 'cmt-top-name')
        cmtNames = [cmtname.text for cmtname in names]

        buy = listComments.find_elements(By.CLASS_NAME, 'confirm-buy')
        confirmBuy = [cfBuy.text for cfBuy in buy]

        contents = listComments.find_elements(By.CLASS_NAME, 'cmt-content')
        cmtContents = [content.text for content in contents]

        likes = listComments.find_elements(By.CLASS_NAME, 'cmt-command')
        cmtLikes = [like.find_element(By.TAG_NAME, 'a').text for like in likes]

        cmtProduct.append(productTitles[i])
#
    except ElementClickInterceptedException:
        cmtNames, confirmBuy, cmtContents, cmtLikes = [], [], [], []

# print(cmtNames)
# print(confirmBuy)
# print(cmtContents)
# print(cmtLikes)

productDetailComments = pd.DataFrame(list(zip(cmtProduct, cmtNames, confirmBuy, cmtContents, cmtLikes)),columns=["Title", "Name", "Confirm Buy", "Content", "Likes"])
# productDetailComments.info()
# print(productDetailComments)

Smartphone = pd.merge(Product, productDetailComments, on="Title", how= "left")

Smartphone.info()
print(Smartphone.head(1).T)
# print(Smartphone)

time.sleep(30)
# driver.quit()


