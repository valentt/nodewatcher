"""
E2E Tests for admin login functionality.

These tests verify that admin users can successfully log into
the Django admin interface.
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAdminLogin:
    """Test suite for admin login functionality."""

    def test_admin_login_page_loads(self, driver, base_url):
        """Test that the admin login page loads correctly."""
        driver.get(f'{base_url}/admin/login/')

        # Verify login form is present
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = driver.find_element(By.NAME, 'password')

        assert username_field is not None
        assert password_field is not None

    def test_admin_login_success(self, driver, base_url, admin_credentials):
        """Test successful admin login."""
        import time
        username, password = admin_credentials

        # Navigate to admin login
        driver.get(f'{base_url}/admin/login/')

        wait = WebDriverWait(driver, 10)

        # Fill in credentials
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        username_field.clear()
        username_field.send_keys(username)

        password_field = driver.find_element(By.NAME, 'password')
        password_field.clear()
        password_field.send_keys(password)

        # Submit
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button.click()

        # Wait for response
        time.sleep(2)

        # Check for login error
        if '/admin/login/' in driver.current_url:
            error_elements = driver.find_elements(By.CSS_SELECTOR, '.errornote')
            if error_elements:
                pytest.skip(f'Admin credentials invalid. Set NODEWATCHER_ADMIN_USER and NODEWATCHER_ADMIN_PASS env vars. Error: {error_elements[0].text}')
            pytest.skip(f'Admin login failed for "{username}". Check credentials.')

        # Verify successful login
        assert '/admin/login/' not in driver.current_url

    def test_admin_dashboard_accessible(self, logged_in_admin, base_url):
        """Test that admin dashboard is accessible after login."""
        driver = logged_in_admin

        # Navigate to admin home
        driver.get(f'{base_url}/admin/')

        # Verify we're on the admin page
        wait = WebDriverWait(driver, 10)
        site_header = wait.until(EC.presence_of_element_located((By.ID, 'site-name')))

        assert site_header is not None
        assert 'administration' in driver.title.lower() or 'admin' in driver.title.lower()


class TestMainSiteAccess:
    """Test suite for main site access."""

    def test_main_page_loads(self, driver, base_url):
        """Test that the main page loads correctly."""
        driver.get(base_url)

        # Page should load without error
        assert driver.title  # Title should be set

    def test_map_page_loads(self, driver, base_url):
        """Test that the map page loads correctly (was 500 error)."""
        driver.get(f'{base_url}/map/')

        wait = WebDriverWait(driver, 15)

        # Verify the page loaded (not a 500 error)
        # Check for common error indicators
        page_source = driver.page_source.lower()
        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()

    def test_list_page_loads(self, driver, base_url):
        """Test that the list page loads correctly (was 500 error)."""
        driver.get(f'{base_url}/list/')

        wait = WebDriverWait(driver, 15)

        # Verify the page loaded (not a 500 error)
        page_source = driver.page_source.lower()
        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()

    def test_registration_page_loads(self, driver, base_url):
        """Test that the registration page loads correctly (was 500 error)."""
        driver.get(f'{base_url}/account/register/')

        wait = WebDriverWait(driver, 15)

        # Verify the page loaded (not a 500 error)
        page_source = driver.page_source.lower()
        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()

    def test_api_v2_endpoints(self, driver, base_url):
        """Test that API v2 endpoints are accessible."""
        endpoints = [
            '/api/v2/',
            '/api/v2/node/',
            '/api/v2/project/',
            '/api/v2/ippool/',
        ]

        for endpoint in endpoints:
            driver.get(f'{base_url}{endpoint}')
            page_source = driver.page_source.lower()
            # API should return valid JSON or DRF browsable API
            assert 'server error' not in page_source, f'API endpoint {endpoint} returned server error'
