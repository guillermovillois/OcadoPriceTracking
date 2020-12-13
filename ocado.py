from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import requests
from bs4 import BeautifulSoup


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# base url
url = 'https://www.ocado.com/webshop/startWebshop.do'

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
driver.refresh()

# move mouse over eaxpandable menu item so categories appear in the html
action = ActionChains(driver)
firstLevelMenu = driver.find_element_by_class_name("primary-bar-link")
action.move_to_element(firstLevelMenu).perform()

# retrieve main categories names + links
categories = []
for each in driver.find_element_by_id('supernavButton_Grocery').find_elements_by_tag_name('a'):
    categories.append(each.get_attribute('href'))
    print(each.get_attribute('href'), each.get_attribute('text'))

# open a category page
driver.get(categories[3])

# retrieve subcategories
subcats = []
for each in driver.find_element_by_class_name('grocery-section').find_elements_by_class_name('level-item-link'):
    subcats.append(each.get_attribute('href'))
    print(each.get_attribute('href'), each.get_attribute('text'))

while check_exists_by_xpath("//button[@class='btn-primary show-more']"):
    fBody.click()
    print(len(driver.find_elements_by_class_name('fops-item')))


products_on_page = BeautifulSoup(
    driver.page_source, 'html.parser').findAll('div', class_='fop-item')
for product in products_on_page[:20]:
    print(product.find('h4', {'class': 'fop-title'}).attrs['title'])
    print(product.attrs['data-sku'])
    print(product.find('div', class_='price-group-wrapper').find('span',
                                                                 {'class': 'fop-price'}).text)
    print('https://www.ocado.com' + product.find('a')['href'])
