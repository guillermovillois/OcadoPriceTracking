from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

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
