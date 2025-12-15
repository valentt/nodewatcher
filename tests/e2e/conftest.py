"""
Pytest configuration and fixtures for Selenium E2E tests.
"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Test configuration
BASE_URL = os.environ.get('NODEWATCHER_URL', 'http://localhost:8000')
ADMIN_USERNAME = os.environ.get('NODEWATCHER_ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.environ.get('NODEWATCHER_ADMIN_PASS', 'admin')
HEADLESS = os.environ.get('SELENIUM_HEADLESS', 'true').lower() == 'true'
BROWSER = os.environ.get('SELENIUM_BROWSER', 'chrome').lower()
IMPLICIT_WAIT = int(os.environ.get('SELENIUM_IMPLICIT_WAIT', '10'))
SCREENSHOT_DIR = os.environ.get('SCREENSHOT_DIR', 'test_screenshots')


def get_chrome_driver(headless=True):
    """Create Chrome WebDriver with appropriate options."""
    options = ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=options)


def get_firefox_driver(headless=True):
    """Create Firefox WebDriver with appropriate options."""
    options = FirefoxOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--width=1920')
    options.add_argument('--height=1080')
    return webdriver.Firefox(options=options)


@pytest.fixture(scope='session')
def driver():
    """
    Create a WebDriver instance for the test session.
    Supports Chrome and Firefox browsers.
    """
    if BROWSER == 'firefox':
        driver = get_firefox_driver(headless=HEADLESS)
    else:
        driver = get_chrome_driver(headless=HEADLESS)

    driver.implicitly_wait(IMPLICIT_WAIT)
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def base_url():
    """Return the base URL for the nodewatcher instance."""
    return BASE_URL


@pytest.fixture(scope='session')
def admin_credentials():
    """Return admin credentials as a tuple (username, password)."""
    return (ADMIN_USERNAME, ADMIN_PASSWORD)


@pytest.fixture
def logged_in_admin(driver, base_url, admin_credentials):
    """
    Fixture that ensures admin user is logged in.
    Returns the driver for convenience.
    """
    username, password = admin_credentials

    # Navigate to admin login
    driver.get(f'{base_url}/admin/login/')

    # Check if already logged in
    if '/admin/login/' not in driver.current_url:
        return driver

    # Fill in login form
    wait = WebDriverWait(driver, 10)

    username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(By.NAME, 'password')
    password_field.clear()
    password_field.send_keys(password)

    # Submit form
    submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    submit_button.click()

    # Wait for login to complete
    wait.until(EC.url_contains('/admin/'))

    return driver


@pytest.fixture
def logged_in_user(driver, base_url, admin_credentials):
    """
    Fixture that ensures user is logged in to the main site.
    Returns the driver for convenience.
    """
    username, password = admin_credentials

    # Navigate to login page
    driver.get(f'{base_url}/account/login/')

    # Check if already logged in by looking for login form
    try:
        wait = WebDriverWait(driver, 3)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
    except:
        # Already logged in
        return driver

    # Fill in login form
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(By.NAME, 'password')
    password_field.clear()
    password_field.send_keys(password)

    # Submit form
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
    submit_button.click()

    # Wait for login to complete
    WebDriverWait(driver, 10).until(
        lambda d: '/account/login/' not in d.current_url
    )

    return driver


@pytest.fixture(scope='session', autouse=True)
def setup_screenshot_dir():
    """Create screenshot directory if it doesn't exist."""
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)


@pytest.fixture
def screenshot_on_failure(driver, request):
    """Take screenshot on test failure."""
    yield
    if request.node.rep_call.failed:
        test_name = request.node.name
        screenshot_path = os.path.join(SCREENSHOT_DIR, f'{test_name}.png')
        driver.save_screenshot(screenshot_path)
        print(f'Screenshot saved to: {screenshot_path}')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot fixture."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


class PageHelper:
    """Helper class for common page operations."""

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def navigate_to(self, path):
        """Navigate to a path relative to base URL."""
        self.driver.get(f'{self.base_url}{path}')

    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present and return it."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_clickable(self, by, value, timeout=10):
        """Wait for an element to be clickable and return it."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))

    def fill_field(self, name, value):
        """Fill a form field by name."""
        field = self.wait_for_element(By.NAME, name)
        field.clear()
        field.send_keys(value)

    def select_option(self, name, value):
        """Select an option from a select field by value."""
        from selenium.webdriver.support.ui import Select
        select = Select(self.wait_for_element(By.NAME, name))
        select.select_by_value(value)

    def select_option_by_text(self, name, text):
        """Select an option from a select field by visible text."""
        from selenium.webdriver.support.ui import Select
        select = Select(self.wait_for_element(By.NAME, name))
        select.select_by_visible_text(text)

    def click_submit(self):
        """Click the submit button."""
        submit = self.wait_for_clickable(By.CSS_SELECTOR, 'input[type="submit"]')
        submit.click()

    def get_success_message(self):
        """Get success message from the page."""
        try:
            msg = self.wait_for_element(By.CSS_SELECTOR, '.messagelist .success, .messages .success, .alert-success')
            return msg.text
        except:
            return None

    def get_error_messages(self):
        """Get error messages from the page."""
        errors = self.driver.find_elements(By.CSS_SELECTOR, '.errorlist li, .messages .error, .alert-danger')
        return [e.text for e in errors]


@pytest.fixture
def page_helper(driver, base_url):
    """Create a PageHelper instance."""
    return PageHelper(driver, base_url)
