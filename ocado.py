import time
from .vars import base_url, scroll_page
import json

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def scrape_products(products_page):
    driver.get(products_page)
    scroll_page(driver)

    # parse the loaded page with Beautifulsoup
    source = BeautifulSoup(driver.page_source, 'html.parser')
    pagecat = source.findAll(
        'a', {'class': 'bc-desktopBreadcrumbsWithMenu__linkWithMenu'})
    category = pagecat[1].text
    subcat = ''.join((source.find('title').text).split('|')[
                     0].replace("'", '').strip().split(' '))
    products_on_page = source.findAll('div', class_='fop-item')

    products = []

    # loop thru every product in the page and append it to a dictionary
    for product in products_on_page:
        if len(product.text) > 0:
            product_name = product.find(
                'h4', {'class': 'fop-title'}).attrs['title']
            sku = product.attrs['data-sku']
            price = product.find(
                'div', class_='price-group-wrapper').find('span', {'class': 'fop-price'}).text
            url = 'https://www.ocado.com' + product.find('a')['href']
            products.append({
                'name': product_name,
                'sku': sku,
                'price': price.replace('£', ''),
                'url': url
            })

    print(category, subcat, len(products_on_page))
    return [category, subcat, products, len(products_on_page)]


start_time = time.time()

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=chrome_options)
driver.get(base_url)

# expand the categories menu
action = ActionChains(driver)
firstLevelMenu = driver.find_element_by_class_name("primary-bar-link")
action.move_to_element(firstLevelMenu).perform()

# wait the menu to load
driver.implicitly_wait(10)
menu = driver.find_element_by_id(
    'supernavButton_Grocery').find_elements_by_tag_name('a')

# retrieve categories urls
url_cat = []
for each in menu:
    url_cat.append(each.get_attribute('href'))
    print(each.get_attribute('href'), each.get_attribute('text'))

categories = {}
products_scraped = 0

# loop thru categories and then subcategories to scrape each product and
# as result it returns a dictionary with all the products
for url in url_cat:
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
        categ = scrape[0]
    categories[categ] = subcategory

print('Total products scraped: ' + str(products_scraped))
print("_--- %s minutes ---_" % (round(time.time() - start_time, 2)/60))

driver.close()

# export the dictionary into a json file
with open('products.json', 'w') as json_file:
    json.dump(categories, json_file)
