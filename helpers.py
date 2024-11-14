import time

import pytest
from selenium.webdriver.common.by import By

def login_standard_user(driver):
    driver.get("https://www.saucedemo.com/")
    perform_login(driver, "standard_user", "secret_sauce")

def login_locked_out_user(driver):
    driver.get("https://www.saucedemo.com/")
    perform_login(driver, "locked_out_user", "secret_sauce")

def login_problem_user(driver):
    driver.get("https://www.saucedemo.com/")
    perform_login(driver, "problem_user", "secret_sauce")

def login_performance_glitch_user(driver):
    driver.get("https://www.saucedemo.com/")
    perform_login(driver, "performance_glitch_user", "secret_sauce")


def login_error_user(driver):
    driver.get("https://www.saucedemo.com/")
    perform_login(driver, "error_user", "secret_sauce")


def login_visual_user(driver):
    driver.get("https://www.saucedemo.com/")
    perform_login(driver, "visual_user", "secret_sauce")


def perform_login(driver, username, password):
    username_input = driver.find_element(By.ID, "user-name")
    username_input.clear()
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys(password)

    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

def open_hamburger(driver):
    hamburger_icon = driver.find_element(By.ID, "react-burger-menu-btn")
    hamburger_icon.click()

user_data = [
    ("standard_user", "secret_sauce"),
    ("locked_out_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce"),
    ("error_user", "secret_sauce"),
    ("visual_user", "secret_sauce")
]

user_data_simple = [
    ("standard_user", "secret_sauce")
]

def skip_user_check(username, password):
    if (username, password) in skip_users:
        pytest.skip(f"Skipping test for {username} because login failed.")

skip_users = [("locked_out_user", "secret_sauce")]

def logout(driver):
    open_hamburger(driver)
    time.sleep(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(1)
    driver.refresh()

def click_all_buttons(driver):
    add_to_cart_button = driver.find_elements(By.XPATH, "//button[text()='Add to cart']")
    initial_add_to_cart_count = len(add_to_cart_button)
    for button in add_to_cart_button:
        button.click()
        time.sleep(1)

    return add_to_cart_button, initial_add_to_cart_count
