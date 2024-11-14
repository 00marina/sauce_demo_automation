import time
from urllib.response import addbase

import pytest
from  selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from helpers import *
from selenium.common.exceptions import NoSuchElementException, TimeoutException

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

#check all homepage add to cart buttons
@pytest.mark.parametrize("username, password", user_data)
def test_button_click(driver, login_first, username, password):
    time.sleep(1)
    add_to_cart_button, initial_add_to_cart_count = click_all_buttons(driver)

    remove_buttons = driver.find_elements(By.XPATH, "//button[text()='Remove']")
    final_remove_count = len(remove_buttons)
    time.sleep(1)

    assert final_remove_count == initial_add_to_cart_count, \
        f"Not all 'Add to Cart' buttons changed to 'Remove' buttons. Expected {initial_add_to_cart_count}, but got {final_remove_count} for {username}"

    logout(driver)

#check if the cart number is a match for number of items user added to the cart
@pytest.mark.parametrize("username, password", user_data)
def test_cart_number(driver, login_first, username, password):
    add_to_cart_button, initial_add_to_cart_count = click_all_buttons(driver)

    cart_number = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    cart_number_value = int(cart_number)

    assert initial_add_to_cart_count == cart_number_value, f'Cart number does not match number of clicked buttons for {username}.'

#check if titles of the items in the cart match the ones user added to the cart
@pytest.mark.parametrize("username, password", user_data)
def test_cart_items(driver, login_first, username, password):
    titles = []
    cart_titles_list = []
    add_to_cart_button = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
    for button in add_to_cart_button:
        parent_element = button.find_element(By.XPATH, "./ancestor::div[contains(@class, 'inventory_item')]")
        title = parent_element.find_element(By.CLASS_NAME, "inventory_item_name ").text
        titles.append(title)
        button.click()


    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()

    if driver.current_url == "https://www.saucedemo.com/cart.html":
        cart_titles = driver.find_elements(By.CLASS_NAME, "inventory_item_name")

        for cart_title in cart_titles:
            cart_title_value = cart_title.text
            cart_titles_list.append(cart_title_value)

        assert cart_titles_list == titles, f"Received titles do not match sent titles for user {username}."
    else:
        assert False, f"Wrong url for user {username}."