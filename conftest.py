import pytest
from helpers import skip_user_check, perform_login

#login function used by many tests
@pytest.fixture(scope="function")
def login_first(driver, username, password):
    skip_user_check(username, password)

    driver.delete_all_cookies()

    if driver.current_url.startswith("http"):
        driver.execute_script('window.localStorage.clear();')

    driver.get("https://www.saucedemo.com/")
    perform_login(driver, username, password)