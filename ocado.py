import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import time
import requests
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import pandas as pd

import requests
from bs4 import BeautifulSoup


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def scrape_products(products_page):
    driver.get(products_page)

    # wait the page to load and check if it has the button "Show More"
    element = WebDriverWait(driver, 10)
    while check_exists_by_xpath("//button[@class='btn-primary show-more']"):
        driver.find_element_by_xpath(
            "//button[@class='btn-primary show-more']").click()
        # print(len(driver.find_elements_by_class_name('fops-item')))

    # Scroll down so all the products load in the html code
    speed = 40
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script(
            "window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")

    # parse the html code with Beautifulsoup
    source = BeautifulSoup(driver.page_source, 'html.parser')
    pagecat = source.findAll(
        'a', {'class': 'bc-desktopBreadcrumbsWithMenu__linkWithMenu'})
    category = pagecat[1].text
    subcat = ''.join((source.find('title').text).split('|')[
                     0].replace("'", '').strip().split(' '))
    products_on_page = source.findAll('div', class_='fop-item')

    products = {}

    # loop thru every product in the page and append it to a dictionary
    for product in products_on_page:
        if len(product.text) > 0:
            product_name = product.find(
                'h4', {'class': 'fop-title'}).attrs['title']
            sku = product.attrs['data-sku']
            price = product.find(
                'div', class_='price-group-wrapper').find('span', {'class': 'fop-price'}).text
            url = 'https://www.ocado.com' + product.find('a')['href']
            products[sku] = {
                'name': product_name,
                'sku': sku,
                'price': price,
                'url': url
            }

    print(category, subcat, len(products_on_page))
    return [category, subcat, products, len(products_on_page)]


start_time = time.time()

url = 'https://www.ocado.com/webshop/startWebshop.do'


chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
# driver.refresh()

# expand categories menu
action = ActionChains(driver)
firstLevelMenu = driver.find_element_by_class_name("primary-bar-link")
action.move_to_element(firstLevelMenu).perform()
# wait
driver.implicitly_wait(10)
menu = driver.find_element_by_id(
    'supernavButton_Grocery').find_elements_by_tag_name('a')


url_cat = []
for each in menu:
    url_cat.append(each.get_attribute('href'))
    print(each.get_attribute('href'), each.get_attribute('text'))


categories = {}
products_scraped = 0

for url in url_cat[-1:]:
    print(url)
    driver.get(url)
    subcats = []
    for each in driver.find_element_by_class_name('grocery-section').find_elements_by_class_name('level-item-link'):
        subcats.append(each.get_attribute('href'))
        # print(each.get_attribute('href'),each.get_attribute('text'))

    subcategory = {}
    for url in subcats:
        scrape = scrape_products(url)
        subcategory[scrape[1]] = scrape[2]
        products_scraped += scrape[3]
        cat = scrape[0]
    categories[cat] = subcategory

print('Total products scraped: ' + str(products_scraped))
print("--- %s seconds ---" % round(time.time() - start_time, 2))


driver.close()
