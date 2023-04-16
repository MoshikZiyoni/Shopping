from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import requests
from urllib.request import urlopen

url = 'http://127.0.0.1:4434/product/api/'

service_obj = Service("C:/Users/moshi/Downloads/chromedriver.exe")

driver = webdriver.Chrome(service=service_obj)

driver.get('https://www.realwatersports.com/collections/surfboards')
driver.maximize_window()
time.sleep(5)
ccc = 0
a = 0
for i in range(30):
    ccc = int(ccc)+1
    a = int(a)+1
    ccc = str(ccc)
    a = str(a)
    print(ccc)
    # driver.find_element(By.XPATH,'').click
    description = driver.find_element(
        By.XPATH, '/html/body/main/div/div[2]/div[2]/div[2]/article['+ccc+']/div/div/h2/a').text
    brand_name = driver.find_element(
        By.XPATH, '/html/body/main/div/div[2]/div[2]/div[2]/article['+ccc+']/div/div/h3').text
    price = driver.find_element(
        By.XPATH, '/html/body/main/div/div[2]/div[2]/div[2]/article['+ccc+']/div/div/div[1]/div[2]/span').text
    try:
        image = driver.find_element(
            By.XPATH, '/html/body/main/div/div[2]/div[2]/div[2]/article['+ccc+']/div/a/figure/img')
        image_url = image.get_attribute("src")
        response = requests.get(image_url)
        image_binary = requests.get(image_url).content
        print('image good')
        with open(a+"image.jpg", "wb") as f:
            f.write(response.content)
        time.sleep(0.5)
    except Exception:
        pass
    try:
        price = price.replace("$", "")

    except Exception:
        "price not good"
        continue
    try:
        price = int(price.replace(",", ""))
    except Exception:
        "price not good"
    data = {
        'name': brand_name,
        'description': description,
        'price': price,
    }

    response = requests.post(url, data=data)

    if response.status_code == 201:
        print('Product created successfully!')
    else:
        print(f'Error creating product: {response.text}')
