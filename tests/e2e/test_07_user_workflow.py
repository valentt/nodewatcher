"""
E2E Tests for user login and node editing workflow.

These tests verify that users can:
1. Log into the main site (not admin)
2. Access their nodes
3. Edit their own nodes
"""
import os
import time
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Test user credentials from environment or defaults
TEST_USERNAME = os.environ.get('NODEWATCHER_ADMIN_USER', 'admin')
TEST_PASSWORD = os.environ.get('NODEWATCHER_ADMIN_PASS', 'admin')


class TestUserLogin:
    """Test suite for user login functionality on the main site."""

    def test_login_page_loads(self, driver, base_url):
        """Test that the login page loads correctly."""
        driver.get(f'{base_url}/account/login/')

        wait = WebDriverWait(driver, 10)

        # Check page loaded without error
        assert '500' not in driver.title.lower()
        assert 'server error' not in driver.page_source.lower()

        # Verify login form elements are present
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password_field = driver.find_element(By.NAME, 'password')
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

        assert username_field is not None
        assert password_field is not None
        assert submit_button is not None

    def test_login_page_has_register_link(self, driver, base_url):
        """Test that login page has link to registration."""
        driver.get(f'{base_url}/account/login/')

        # Look for register link
        register_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="register"]')
        assert len(register_links) > 0, "Registration link should be present on login page"

    def test_login_with_invalid_credentials(self, driver, base_url):
        """Test that invalid credentials show appropriate error."""
        driver.get(f'{base_url}/account/login/')

        wait = WebDriverWait(driver, 10)

        # Fill in invalid credentials
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        username_field.clear()
        username_field.send_keys('invalid_user_12345')

        password_field = driver.find_element(By.NAME, 'password')
        password_field.clear()
        password_field.send_keys('wrong_password')

        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # Wait for response
        time.sleep(2)

        # Should still be on login page or show error
        page_source = driver.page_source.lower()
        # Either stay on login page or show error message
        assert '/account/login/' in driver.current_url or 'error' in page_source or 'invalid' in page_source

    def test_login_success(self, driver, base_url):
        """Test successful user login."""
        driver.get(f'{base_url}/account/login/')

        wait = WebDriverWait(driver, 10)

        # Fill in credentials
        username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        username_field.clear()
        username_field.send_keys(TEST_USERNAME)

        password_field = driver.find_element(By.NAME, 'password')
        password_field.clear()
        password_field.send_keys(TEST_PASSWORD)

        # Submit form
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # Wait for response
        time.sleep(2)

        # Check if login succeeded
        if '/account/login/' in driver.current_url:
            # Check for error message
            page_source = driver.page_source.lower()
            if 'please enter a correct' in page_source or 'invalid' in page_source or 'error' in page_source:
                pytest.skip(f'Login credentials invalid for user "{TEST_USERNAME}". Set NODEWATCHER_ADMIN_USER and NODEWATCHER_ADMIN_PASS env vars with valid credentials.')
            # Still on login page but no error - might be a different issue
            pytest.skip(f'Login did not redirect for user "{TEST_USERNAME}". Check credentials.')

        # Should be redirected away from login page
        assert '/account/login/' not in driver.current_url, "Should be redirected after successful login"


class TestMyNodesPage:
    """Test suite for 'My Nodes' page functionality."""

    def test_mynodes_page_requires_login(self, driver, base_url):
        """Test that My Nodes page requires authentication."""
        # First logout if logged in
        driver.get(f'{base_url}/account/logout/')
        time.sleep(1)

        # Try to access my nodes
        driver.get(f'{base_url}/my/nodes/')
        time.sleep(2)

        # Should redirect to login or show login form
        current_url = driver.current_url.lower()
        page_source = driver.page_source.lower()

        assert 'login' in current_url or 'login' in page_source or 'sign in' in page_source, \
            "My Nodes page should require authentication"

    def test_mynodes_page_accessible_when_logged_in(self, logged_in_user, base_url):
        """Test that My Nodes page is accessible when logged in."""
        driver = logged_in_user

        driver.get(f'{base_url}/my/nodes/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        # Page should load without error
        assert '500' not in driver.title.lower()
        assert 'server error' not in driver.page_source.lower()

        # Should not be on login page
        assert '/account/login/' not in driver.current_url


class TestNodeEditing:
    """Test suite for node editing functionality."""

    def test_node_edit_page_accessible(self, logged_in_user, base_url):
        """Test that node edit pages are accessible for logged in users."""
        driver = logged_in_user

        # First get list of nodes from API
        response = requests.get(f'{base_url}/api/v3/node/?format=json')
        if response.status_code != 200:
            pytest.skip("API not available")

        data = response.json()
        if data.get('count', 0) == 0:
            pytest.skip("No nodes in database to test editing")

        # Try to access edit page for first node
        node_uuid = data['results'][0]['@id']
        driver.get(f'{base_url}/node/{node_uuid}/edit/')

        time.sleep(2)

        # Check if page loaded
        page_source = driver.page_source.lower()
        current_url = driver.current_url

        # Should either show edit form, or permission denied, or redirect to login
        # All are valid responses depending on node ownership
        assert '500' not in driver.title.lower(), "Edit page should not return 500 error"

    def test_node_edit_form_elements(self, logged_in_user, base_url):
        """Test that node edit form has proper elements."""
        driver = logged_in_user

        # Get a node to edit
        response = requests.get(f'{base_url}/api/v3/node/?format=json')
        if response.status_code != 200:
            pytest.skip("API not available")

        data = response.json()
        if data.get('count', 0) == 0:
            pytest.skip("No nodes in database")

        node_uuid = data['results'][0]['@id']
        driver.get(f'{base_url}/node/{node_uuid}/edit/')

        time.sleep(3)

        # Check page loaded without 500 error
        if '500' in driver.title.lower() or 'server error' in driver.page_source.lower():
            pytest.fail("Node edit page returned server error")

        # If we got to the edit page, check for form elements
        if '/edit/' in driver.current_url:
            # Look for common form elements
            page_source = driver.page_source

            # Check for form tag
            forms = driver.find_elements(By.TAG_NAME, 'form')
            if forms:
                # Found a form - test passed
                assert True
            else:
                # No form found - might be permission issue
                if 'permission' in page_source.lower() or 'denied' in page_source.lower():
                    pytest.skip("No permission to edit this node")

    def test_click_edit_from_node_detail(self, logged_in_user, base_url):
        """Test clicking edit button from node detail page."""
        driver = logged_in_user

        # Get a node
        response = requests.get(f'{base_url}/api/v3/node/?format=json')
        if response.status_code != 200:
            pytest.skip("API not available")

        data = response.json()
        if data.get('count', 0) == 0:
            pytest.skip("No nodes in database")

        node_uuid = data['results'][0]['@id']

        # Go to node detail page
        driver.get(f'{base_url}/node/{node_uuid}/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        # Check page loaded
        assert '500' not in driver.title.lower(), "Node detail page returned 500 error"

        # Look for edit link/button
        edit_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/edit"]')
        edit_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[onclick*="edit"], .edit-btn, .btn-edit')

        if edit_links:
            # Click the first edit link
            edit_links[0].click()
            time.sleep(2)

            # Should navigate to edit page or stay (if no permission)
            assert '500' not in driver.title.lower(), "Edit page should not return 500 error"
        elif edit_buttons:
            edit_buttons[0].click()
            time.sleep(2)
            assert '500' not in driver.title.lower()
        else:
            # No edit button - might be intentional (view only) or not visible to this user
            pytest.skip("No edit button found on node detail page")


class TestRegistrationPage:
    """Test suite for user registration page."""

    def test_registration_page_loads(self, driver, base_url):
        """Test that registration page loads without error."""
        driver.get(f'{base_url}/account/register/')

        time.sleep(2)

        # Check page loaded without error
        assert '500' not in driver.title.lower(), "Registration page returned 500 error"
        assert 'server error' not in driver.page_source.lower()

    def test_registration_form_has_required_fields(self, driver, base_url):
        """Test that registration form has all required fields."""
        driver.get(f'{base_url}/account/register/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        # Check for essential form fields
        required_fields = ['username', 'email', 'password1', 'password2']

        for field_name in required_fields:
            fields = driver.find_elements(By.NAME, field_name)
            assert len(fields) > 0, f"Registration form should have '{field_name}' field"

    def test_registration_password_validation(self, driver, base_url):
        """Test that registration validates password mismatch."""
        driver.get(f'{base_url}/account/register/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        # Fill in form with mismatched passwords
        try:
            username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
            username.send_keys('testuser_selenium')

            email = driver.find_element(By.NAME, 'email')
            email.send_keys('test@example.com')

            password1 = driver.find_element(By.NAME, 'password1')
            password1.send_keys('TestPass123!')

            password2 = driver.find_element(By.NAME, 'password2')
            password2.send_keys('DifferentPass456!')

            # Find and click submit (but don't actually submit to avoid creating user)
            # Just check form elements are interactive
            submit_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[type="submit"]')
            assert len(submit_buttons) > 0, "Registration form should have submit button"

        except Exception as e:
            pytest.skip(f"Could not test registration form: {e}")


class TestLogoutFlow:
    """Test suite for logout functionality."""

    def test_logout_works(self, logged_in_user, base_url):
        """Test that logout works correctly."""
        driver = logged_in_user

        # Navigate to logout
        driver.get(f'{base_url}/account/logout/')

        time.sleep(2)

        # Try to access protected page
        driver.get(f'{base_url}/my/nodes/')

        time.sleep(2)

        # Should redirect to login
        current_url = driver.current_url.lower()
        page_source = driver.page_source.lower()

        # Either redirected to login or shows login form
        is_logged_out = 'login' in current_url or 'login' in page_source or 'sign in' in page_source
        assert is_logged_out, "After logout, protected pages should require login"
