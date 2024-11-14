import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from helpers import *

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

#testing sorting options of the items on the homepage
@pytest.mark.parametrize("username, password", user_data)
@pytest.mark.parametrize("menu_action, target_element, expected_result", [
    ("//*[@id='header_container']/div[2]/div/span/select/option[2]", "inventory_item_name", "is_descending"),
    ("//*[@id='header_container']/div[2]/div/span/select/option[3]", "inventory_item_price", "is_ascending"),
    ("//*[@id='header_container']/div[2]/div/span/select/option[4]", "inventory_item_price", "is_descending"),
    ("//*[@id='header_container']/div[2]/div/span/select/option[1]", "inventory_item_name", "is_ascending")
])
def test_filters(driver, username, password, login_first, menu_action, target_element, expected_result):
    filter_menu = driver.find_element(By. CLASS_NAME, "product_sort_container")
    filter_menu.click()
    option = driver.find_element(By. XPATH, menu_action)
    option.click()

    inventory = []

    inventory_titles = driver.find_elements(By. CLASS_NAME, target_element)
    for item in inventory_titles:
        if target_element == "inventory_item_price":
            price = item.text.strip("$")
            inventory.append(float(price))
        else:
            inventory.append(item.text)

    is_ascending = inventory == sorted(inventory)
    is_descending  = inventory == sorted(inventory, reverse=True)
    if expected_result == "is_ascending":
        assert is_ascending, f"Inventory is not ascending for {target_element} un user {username}."
    else:
        assert is_descending, f"Inventory is not descending for {target_element} un user {username}."