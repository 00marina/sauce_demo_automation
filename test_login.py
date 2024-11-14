import pytest
from selenium import webdriver
from helpers import login_standard_user, login_problem_user, login_visual_user, login_error_user, login_locked_out_user, \
    login_performance_glitch_user, perform_login, skip_user_check


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.skip_user_check
@pytest.mark.parametrize("login_function, expected_url", [
    (login_standard_user, "https://www.saucedemo.com/inventory.html"),
    (login_locked_out_user, "https://www.saucedemo.com/"),
    (login_problem_user, "https://www.saucedemo.com/inventory.html"),
    (login_performance_glitch_user, "https://www.saucedemo.com/inventory.html"),
    (login_error_user, "https://www.saucedemo.com/inventory.html"),
    (login_visual_user, "https://www.saucedemo.com/inventory.html"),
])
def test_user_login(driver, login_function, expected_url):
    login_function(driver)
    actual_url = driver.current_url
    assert actual_url == expected_url
