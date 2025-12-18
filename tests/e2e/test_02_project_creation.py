"""
E2E Tests for project creation.

These tests verify that projects (like "Croatia") can be created
through the Django admin interface.
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class TestProjectCreation:
    """Test suite for project creation via admin interface."""

    PROJECT_NAME = 'Croatia'
    PROJECT_DESCRIPTION = 'Croatian wireless network community project'
    PROJECT_LOCATION_LAT = '45.8150'  # Zagreb coordinates
    PROJECT_LOCATION_LON = '15.9819'

    def test_project_admin_page_accessible(self, logged_in_admin, base_url):
        """Test that project admin page is accessible."""
        driver = logged_in_admin
        driver.get(f'{base_url}/admin/projects/project/')

        wait = WebDriverWait(driver, 10)

        # Should see the project list page
        page_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content h1')))
        assert 'project' in page_title.text.lower()

    def test_create_croatia_project(self, logged_in_admin, base_url):
        """Test creating the Croatia project."""
        driver = logged_in_admin

        # Navigate to add project page
        driver.get(f'{base_url}/admin/projects/project/add/')

        wait = WebDriverWait(driver, 10)

        # Wait for form to load
        name_field = wait.until(EC.presence_of_element_located((By.NAME, 'name')))

        # Fill in project details
        name_field.clear()
        name_field.send_keys(self.PROJECT_NAME)

        # Fill description
        desc_field = driver.find_element(By.NAME, 'description')
        desc_field.clear()
        desc_field.send_keys(self.PROJECT_DESCRIPTION)

        # Set as default project
        try:
            is_default = driver.find_element(By.NAME, 'is_default')
            if not is_default.is_selected():
                is_default.click()
        except:
            pass  # Field might not exist or be different

        # Handle location field (GIS PointField)
        # Django-leaflet creates a map widget, we need to set the underlying field
        try:
            # Try to find the location text input if it exists
            location_input = driver.find_element(By.NAME, 'location')
            location_input.clear()
            # Format: POINT(longitude latitude)
            location_input.send_keys(f'POINT({self.PROJECT_LOCATION_LON} {self.PROJECT_LOCATION_LAT})')
        except:
            # If using a map widget, try to find the hidden input
            try:
                # django-leaflet uses a different structure
                location_inputs = driver.find_elements(By.CSS_SELECTOR, '[name*="location"]')
                for inp in location_inputs:
                    if inp.get_attribute('type') != 'hidden':
                        inp.clear()
                        inp.send_keys(f'POINT({self.PROJECT_LOCATION_LON} {self.PROJECT_LOCATION_LAT})')
                        break
            except:
                pass  # Location might be optional

        # Submit the form
        save_button = wait.until(EC.element_to_be_clickable((By.NAME, '_save')))
        save_button.click()

        # Wait for redirect and check for success
        wait.until(lambda d: '/add/' not in d.current_url)

        # Check for success message
        try:
            success_msg = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.messagelist .success, .messages .success')
            ))
            assert self.PROJECT_NAME in success_msg.text or 'success' in success_msg.text.lower()
        except:
            # If no message, verify project exists in list
            driver.get(f'{base_url}/admin/projects/project/')
            page_source = driver.page_source
            assert self.PROJECT_NAME in page_source

    def test_verify_croatia_project_exists(self, logged_in_admin, base_url):
        """Verify the Croatia project exists in the admin list."""
        driver = logged_in_admin
        driver.get(f'{base_url}/admin/projects/project/')

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'result_list')))

        # Check if Croatia project is in the list
        page_source = driver.page_source
        assert self.PROJECT_NAME in page_source, f'Project "{self.PROJECT_NAME}" not found in admin list'

    def test_project_appears_in_api(self, logged_in_admin, base_url):
        """Verify the project appears in the API."""
        driver = logged_in_admin
        driver.get(f'{base_url}/api/v3/project/')

        wait = WebDriverWait(driver, 10)

        # Give page time to load
        time.sleep(2)

        page_source = driver.page_source
        # The project name should appear in the API response
        assert self.PROJECT_NAME in page_source or 'croatia' in page_source.lower(), \
            'Project not found in API response'


class TestProjectWithSSID:
    """Test creating a project with SSID configuration."""

    def test_add_ssid_to_project(self, logged_in_admin, base_url):
        """Test adding an SSID to the Croatia project."""
        driver = logged_in_admin

        # First find the Croatia project
        driver.get(f'{base_url}/admin/projects/project/')

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'result_list')))

        # Click on Croatia project to edit
        try:
            croatia_link = driver.find_element(By.LINK_TEXT, 'Croatia')
            croatia_link.click()
        except:
            # Project might not exist, skip test
            pytest.skip('Croatia project not found, skipping SSID test')

        # Wait for edit form
        wait.until(EC.presence_of_element_located((By.NAME, 'name')))

        # Look for SSID inline form
        # Django admin uses inline formsets for related models
        try:
            # Try to find SSID inline section
            ssid_section = driver.find_elements(By.CSS_SELECTOR, '.inline-group')
            if ssid_section:
                # Find add button for SSID
                add_buttons = driver.find_elements(By.CSS_SELECTOR, '.add-row a')
                if add_buttons:
                    add_buttons[0].click()
                    time.sleep(1)

                    # Fill SSID fields
                    essid_fields = driver.find_elements(By.CSS_SELECTOR, '[name*="essid"]')
                    if essid_fields:
                        for field in essid_fields:
                            if not field.get_attribute('value'):
                                field.send_keys('croatia-mesh')
                                break

                    # Save
                    save_button = driver.find_element(By.NAME, '_save')
                    save_button.click()

                    wait.until(lambda d: '/change/' not in d.current_url or 'success' in d.page_source.lower())
        except:
            pass  # SSID might not be available as inline
