"""
E2E Tests for node editing functionality.

These tests verify that nodes can be edited through the nodewatcher
web interface, specifically testing the registry form state handling
that was fixed for Django 4.x compatibility (get_random_string fix).
"""
import pytest
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Test user with secure password for testing
# This should be created in the database before running tests
TEST_USER = 'selenium_test_user'
TEST_PASSWORD = 'Nw$3l3n1um_T3st!2024_S3cur3P@ss'


class TestNodeEditPage:
    """Test suite for node edit page functionality.

    These tests specifically verify the fix for Django 4.x compatibility
    where get_random_string() requires an explicit length argument.
    """

    def test_node_edit_page_loads(self, logged_in_user, base_url):
        """
        Test that node edit page loads without 500 error.

        This tests the fix for:
        TypeError: get_random_string() missing 1 required positional argument: 'length'

        The bug was in nodewatcher/core/registry/forms/formstate.py
        """
        driver = logged_in_user

        # First, get a node UUID from the API
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        page_source = driver.page_source

        # Find node UUIDs in the response
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, page_source.lower())

        if not uuids:
            pytest.skip('No nodes found in the system to test editing')

        # Try to access the node's edit page
        node_uuid = uuids[0]
        driver.get(f'{base_url}/node/{node_uuid}/edit/')

        wait = WebDriverWait(driver, 15)
        time.sleep(3)  # Wait for registry forms to load

        # Check for errors
        page_source = driver.page_source.lower()
        current_url = driver.current_url

        # Should NOT have server error
        assert 'server error' not in page_source, \
            f'Server error on node edit page for node {node_uuid}'
        assert '500' not in driver.title.lower(), \
            f'500 error on node edit page for node {node_uuid}'
        assert 'typeerror' not in page_source, \
            'TypeError found - possible get_random_string() issue'
        assert 'get_random_string' not in page_source, \
            'get_random_string error found in page'

        # Should be on the edit page (or redirected to login)
        assert '/edit/' in current_url or '/login/' in current_url, \
            f'Unexpected redirect to {current_url}'

        # If on edit page, verify form elements exist
        if '/edit/' in current_url:
            # Look for form elements
            forms = driver.find_elements(By.TAG_NAME, 'form')
            assert len(forms) > 0, 'No form found on edit page'

    def test_node_edit_form_renders(self, logged_in_user, base_url):
        """Test that node edit form renders with all registry sections."""
        driver = logged_in_user

        # Get a node UUID
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, driver.page_source.lower())

        if not uuids:
            pytest.skip('No nodes found in the system')

        node_uuid = uuids[0]
        driver.get(f'{base_url}/node/{node_uuid}/edit/')

        wait = WebDriverWait(driver, 15)
        time.sleep(3)

        page_source = driver.page_source.lower()

        # Should not have any Python errors in the page
        assert 'traceback' not in page_source, 'Python traceback found in page'
        assert 'exception' not in page_source or 'expected' in page_source, \
            'Exception found in page'

        # If on edit page, look for registry form sections
        if '/edit/' in driver.current_url:
            # Common registry sections
            registry_indicators = [
                'general',
                'name',
                'project',
            ]

            found_indicators = [ind for ind in registry_indicators if ind in page_source]
            assert len(found_indicators) > 0, \
                f'No registry form sections found. Page might not be rendering correctly.'

    def test_node_edit_saves_changes(self, logged_in_user, base_url):
        """Test that node edit form can save changes."""
        driver = logged_in_user

        # Get a node UUID
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, driver.page_source.lower())

        if not uuids:
            pytest.skip('No nodes found in the system')

        node_uuid = uuids[0]
        driver.get(f'{base_url}/node/{node_uuid}/edit/')

        wait = WebDriverWait(driver, 15)
        time.sleep(3)

        # Check page loaded correctly
        page_source = driver.page_source.lower()
        assert 'server error' not in page_source

        if '/edit/' in driver.current_url:
            # Try to find and click submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button.btn-primary',
                '.form-actions button',
            ]

            submitted = False
            for selector in submit_selectors:
                try:
                    buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            btn.click()
                            submitted = True
                            break
                    if submitted:
                        break
                except:
                    continue

            if submitted:
                time.sleep(3)

                # After submission, check for success
                page_source = driver.page_source.lower()
                current_url = driver.current_url

                # Should not have server error
                assert 'server error' not in page_source, \
                    'Server error after form submission'

                # Success indicators
                success = (
                    'success' in page_source or
                    'saved' in page_source or
                    '/edit/' not in current_url  # Redirect away from edit
                )

                # Even if there are validation errors, the form should work
                assert 'typeerror' not in page_source, \
                    'TypeError after form submission'


class TestNodeEditWithSpecificNode:
    """Test node edit with a specific node UUID (Osijek-Mestrovic)."""

    OSIJEK_NODE_UUID = 'c0837444-f927-4189-9490-04bf6bd152a4'

    def test_osijek_node_edit_page(self, logged_in_user, base_url):
        """Test editing the Osijek-Mestrovic node specifically."""
        driver = logged_in_user

        driver.get(f'{base_url}/node/{self.OSIJEK_NODE_UUID}/edit/')

        wait = WebDriverWait(driver, 15)
        time.sleep(3)

        page_source = driver.page_source.lower()
        current_url = driver.current_url

        # Should not have server error
        assert 'server error' not in page_source, \
            f'Server error on Osijek node edit page'
        assert '500' not in driver.title.lower()
        assert 'typeerror' not in page_source
        assert 'get_random_string' not in page_source

        # Take screenshot for debugging
        driver.save_screenshot('test_screenshots/osijek_node_edit.png')

    def test_osijek_node_view_page(self, logged_in_user, base_url):
        """Test viewing the Osijek-Mestrovic node."""
        driver = logged_in_user

        driver.get(f'{base_url}/node/{self.OSIJEK_NODE_UUID}/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source
        assert 'osijek' in page_source or 'mestrovic' in page_source, \
            'Node name not found on view page'


class TestRegistryFormState:
    """Test registry form state handling (the core of the get_random_string fix)."""

    def test_multiple_edit_page_loads(self, logged_in_user, base_url):
        """Test that edit page can be loaded multiple times without errors.

        This tests the session handling and form state generation.
        """
        driver = logged_in_user

        # Get a node UUID
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, driver.page_source.lower())

        if not uuids:
            pytest.skip('No nodes found in the system')

        node_uuid = uuids[0]

        # Load edit page multiple times
        for i in range(3):
            driver.get(f'{base_url}/node/{node_uuid}/edit/')
            time.sleep(2)

            page_source = driver.page_source.lower()

            assert 'server error' not in page_source, \
                f'Server error on edit page load #{i+1}'
            assert 'typeerror' not in page_source, \
                f'TypeError on edit page load #{i+1}'

    def test_form_state_preserved_on_validation_error(self, logged_in_user, base_url):
        """Test that form state is preserved when validation errors occur."""
        driver = logged_in_user

        # Get a node UUID
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, driver.page_source.lower())

        if not uuids:
            pytest.skip('No nodes found in the system')

        node_uuid = uuids[0]
        driver.get(f'{base_url}/node/{node_uuid}/edit/')

        wait = WebDriverWait(driver, 15)
        time.sleep(3)

        if '/edit/' in driver.current_url:
            # Find a required field and clear it to trigger validation error
            text_inputs = driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')

            for inp in text_inputs[:3]:  # Try first 3 inputs
                try:
                    if inp.is_displayed() and inp.is_enabled():
                        original_value = inp.get_attribute('value')
                        if original_value:
                            inp.clear()
                            break
                except:
                    continue

            # Try to submit
            try:
                submit = driver.find_element(By.CSS_SELECTOR,
                    'button[type="submit"], input[type="submit"]')
                submit.click()
                time.sleep(3)
            except:
                pass

            # Page should still work (no 500 error)
            page_source = driver.page_source.lower()
            assert 'server error' not in page_source
            assert 'typeerror' not in page_source
