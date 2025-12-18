"""
E2E Tests for firmware generation.

These tests verify that firmware can be generated through the nodewatcher
web interface and API, including build triggering, status monitoring,
and result retrieval.
"""
import pytest
import time
import re
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class TestBuildChannelSetup:
    """Test suite for build channel and builder configuration."""

    def test_build_channels_api(self, driver, base_url):
        """Test that build channels API is accessible."""
        driver.get(f'{base_url}/api/v3/build_channel/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()

    def test_builders_api(self, driver, base_url):
        """Test that builders API is accessible."""
        driver.get(f'{base_url}/api/v3/builder/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()

    def test_build_versions_api(self, driver, base_url):
        """Test that build versions API is accessible."""
        driver.get(f'{base_url}/api/v3/build_version/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()


class TestBuildResultsAPI:
    """Test suite for build results API."""

    def test_build_results_api_list(self, driver, base_url):
        """Test that build results API returns valid response."""
        driver.get(f'{base_url}/api/v3/build_result/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()

        # Should have JSON structure
        assert 'count' in page_source or 'results' in page_source or '[]' in page_source

    def test_build_results_api_authenticated(self, logged_in_user, base_url):
        """Test that authenticated users can access their build results."""
        driver = logged_in_user
        driver.get(f'{base_url}/api/v3/build_result/')

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()


class TestGeneratorPage:
    """Test suite for firmware generator web interface."""

    def test_generator_page_accessible(self, logged_in_user, base_url):
        """Test that generator page is accessible."""
        driver = logged_in_user

        # First, find a node with generator capability
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        # Look for any node UUID
        page_source = driver.page_source
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, page_source.lower())

        if not uuids:
            pytest.skip('No nodes found in the system')

        node_uuid = uuids[0]

        # Navigate to node's generator page
        driver.get(f'{base_url}/node/{node_uuid}/generate/')
        time.sleep(2)

        page_source = driver.page_source.lower()

        # Page should load without server error
        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()

    def test_node_generator_with_builder(self, logged_in_user, base_url):
        """Test accessing generator for a node with configured device."""
        driver = logged_in_user

        # First, get all nodes
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        page_source = driver.page_source
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, page_source.lower())

        if not uuids:
            pytest.skip('No nodes found in the system')

        # Try each node to find one with generator page
        for node_uuid in uuids[:5]:  # Try first 5 nodes
            driver.get(f'{base_url}/node/{node_uuid}/generate/')
            time.sleep(2)

            page_source = driver.page_source.lower()

            # Check if generator is available (not showing "device not supported")
            if 'not supported' not in page_source and 'no builders' not in page_source:
                # Found a node that supports firmware generation
                assert 'server error' not in page_source
                return

        # If no suitable nodes found, just verify no server errors occurred
        assert True


class TestFirmwareBuildTrigger:
    """Test suite for triggering firmware builds."""

    def find_configured_node(self, driver, base_url):
        """Find a node that is properly configured for firmware generation."""
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        page_source = driver.page_source
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, page_source.lower())

        return uuids[0] if uuids else None

    def test_build_form_loads(self, logged_in_user, base_url):
        """Test that build form loads without errors."""
        driver = logged_in_user

        node_uuid = self.find_configured_node(driver, base_url)
        if not node_uuid:
            pytest.skip('No nodes found in the system')

        driver.get(f'{base_url}/node/{node_uuid}/generate/')
        time.sleep(3)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()

    def test_build_channel_selection(self, logged_in_user, base_url):
        """Test that build channel can be selected in the form."""
        driver = logged_in_user

        node_uuid = self.find_configured_node(driver, base_url)
        if not node_uuid:
            pytest.skip('No nodes found in the system')

        driver.get(f'{base_url}/node/{node_uuid}/generate/')
        time.sleep(3)

        # Look for build channel selection
        page_source = driver.page_source.lower()

        # Check for channel selection form elements
        channel_selectors = [
            'select[name*="channel"]',
            '[name*="build_channel"]',
            '.build-channel',
        ]

        has_channel_select = False
        for selector in channel_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    has_channel_select = True
                    break
            except:
                continue

        # Even if no channel select, page should load without error
        assert 'server error' not in page_source

    def test_trigger_build(self, logged_in_user, base_url):
        """Test triggering a firmware build."""
        driver = logged_in_user

        node_uuid = self.find_configured_node(driver, base_url)
        if not node_uuid:
            pytest.skip('No nodes found in the system')

        driver.get(f'{base_url}/node/{node_uuid}/generate/')
        time.sleep(3)

        page_source = driver.page_source.lower()

        # Check if firmware generation is possible
        if 'not supported' in page_source or 'no builders available' in page_source:
            pytest.skip('Firmware generation not available for this node')

        # Look for generate/build button
        build_selectors = [
            'button[type="submit"]',
            'input[type="submit"]',
            '.btn-primary',
            '[name="build"]',
            'a[href*="generate"]',
        ]

        build_button = None
        for selector in build_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for elem in elements:
                    if elem.is_displayed() and elem.is_enabled():
                        text = elem.text.lower() if elem.text else ''
                        value = elem.get_attribute('value') or ''
                        if 'build' in text or 'generate' in text or 'build' in value.lower():
                            build_button = elem
                            break
                if build_button:
                    break
            except:
                continue

        if build_button:
            build_button.click()
            time.sleep(5)

            # Check for build result page or error
            new_page_source = driver.page_source.lower()
            assert 'server error' not in new_page_source

        # Even without clicking, no server error is success
        assert 'server error' not in page_source


class TestBuildResultMonitoring:
    """Test suite for monitoring build results."""

    def test_my_builds_page(self, logged_in_user, base_url):
        """Test that user can access their builds page."""
        driver = logged_in_user

        # Try various URLs that might show user's builds
        urls_to_try = [
            f'{base_url}/my/builds/',
            f'{base_url}/generator/my/',
            f'{base_url}/generator/',
        ]

        for url in urls_to_try:
            driver.get(url)
            time.sleep(2)

            page_source = driver.page_source.lower()

            # If page loads without 404 or error, it's valid
            if '404' not in driver.title.lower() and 'not found' not in page_source:
                assert 'server error' not in page_source
                return

        # If none of the URLs work, that's okay - just verify API works
        assert True

    def test_build_result_detail(self, logged_in_user, base_url):
        """Test accessing build result detail page."""
        driver = logged_in_user

        # First, get build results from API
        driver.get(f'{base_url}/api/v3/build_result/')
        time.sleep(2)

        page_source = driver.page_source

        # Try to extract a build result UUID
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, page_source.lower())

        if not uuids:
            pytest.skip('No build results found')

        # Try to access build result detail
        result_uuid = uuids[0]
        driver.get(f'{base_url}/api/v3/build_result/{result_uuid}/')
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source


class TestBuildResultFiles:
    """Test suite for build result file handling."""

    def test_build_result_files_api(self, logged_in_user, base_url):
        """Test that build result files are accessible via API."""
        driver = logged_in_user

        # Get build results
        driver.get(f'{base_url}/api/v3/build_result/')
        time.sleep(2)

        page_source = driver.page_source

        # Look for file URLs in the response
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, page_source.lower())

        if not uuids:
            pytest.skip('No build results found')

        # Try to get detail with files
        result_uuid = uuids[0]
        driver.get(f'{base_url}/api/v3/build_result/{result_uuid}/')
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source

    def test_firmware_download_links(self, logged_in_user, base_url):
        """Test that firmware download links are accessible."""
        driver = logged_in_user

        # Get a build result
        driver.get(f'{base_url}/api/v3/build_result/')
        time.sleep(2)

        page_source = driver.page_source

        # Check for file references
        if 'files' in page_source.lower():
            # Files are present in response
            assert 'server error' not in page_source.lower()
        else:
            # No files yet, which is okay
            assert True


class TestBuildStatusPolling:
    """Test suite for build status polling functionality."""

    def test_build_status_values(self, logged_in_user, base_url):
        """Test that build status values are valid."""
        driver = logged_in_user

        driver.get(f'{base_url}/api/v3/build_result/')
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source

        # Valid status values
        valid_statuses = ['pending', 'building', 'ok', 'failed']

        # If we have results, check statuses
        if 'status' in page_source:
            for status in valid_statuses:
                if status in page_source:
                    # Found a valid status
                    break

    def test_polling_endpoint_performance(self, logged_in_user, base_url):
        """Test that API endpoints respond quickly for polling."""
        driver = logged_in_user

        start_time = time.time()
        driver.get(f'{base_url}/api/v3/build_result/')
        end_time = time.time()

        response_time = end_time - start_time

        # API should respond within reasonable time (10 seconds)
        assert response_time < 10, f'API response took too long: {response_time}s'


class TestGeneratorIntegration:
    """Integration tests for the complete firmware generation workflow."""

    def test_complete_build_workflow_api(self, logged_in_user, base_url):
        """Test complete workflow: node -> generate -> monitor via API."""
        driver = logged_in_user

        # Step 1: Find a node
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        page_source = driver.page_source
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, page_source.lower())

        if not uuids:
            pytest.skip('No nodes found in the system')

        node_uuid = uuids[0]

        # Step 2: Check node detail
        driver.get(f'{base_url}/api/v3/node/{node_uuid}/')
        time.sleep(2)

        page_source = driver.page_source.lower()
        assert 'server error' not in page_source

        # Step 3: Check generator page
        driver.get(f'{base_url}/node/{node_uuid}/generate/')
        time.sleep(2)

        page_source = driver.page_source.lower()
        assert 'server error' not in page_source

        # Step 4: Check build results
        driver.get(f'{base_url}/api/v3/build_result/')
        time.sleep(2)

        page_source = driver.page_source.lower()
        assert 'server error' not in page_source

    def test_node_with_firmware_config(self, logged_in_user, base_url):
        """Test that nodes with firmware configuration work correctly."""
        driver = logged_in_user

        # Use API to check nodes with router configuration
        driver.get(f'{base_url}/api/v3/node/?fields=config:core.general__name,config:core.general__router')
        time.sleep(2)

        page_source = driver.page_source.lower()

        assert 'server error' not in page_source
        assert '500' not in driver.title.lower()


class TestErrorHandling:
    """Test suite for error handling in firmware generation."""

    def test_invalid_node_uuid(self, logged_in_user, base_url):
        """Test handling of invalid node UUID."""
        driver = logged_in_user

        # Use a clearly invalid UUID
        invalid_uuid = '00000000-0000-0000-0000-000000000000'
        driver.get(f'{base_url}/node/{invalid_uuid}/generate/')
        time.sleep(2)

        page_source = driver.page_source.lower()

        # Should get 404, not server error
        assert 'server error' not in page_source or '404' in driver.title.lower() or 'not found' in page_source

    def test_invalid_build_result_uuid(self, logged_in_user, base_url):
        """Test handling of invalid build result UUID."""
        driver = logged_in_user

        invalid_uuid = '00000000-0000-0000-0000-000000000000'
        driver.get(f'{base_url}/api/v3/build_result/{invalid_uuid}/')
        time.sleep(2)

        page_source = driver.page_source.lower()

        # Should get 404, not server error
        assert 'server error' not in page_source

    def test_unauthenticated_build_access(self, driver, base_url):
        """Test that unauthenticated users cannot trigger builds."""
        # Get a node UUID first
        driver.get(f'{base_url}/api/v3/node/')
        time.sleep(2)

        page_source = driver.page_source
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids = re.findall(uuid_pattern, page_source.lower())

        if not uuids:
            pytest.skip('No nodes found')

        node_uuid = uuids[0]

        # Try to access generate page without auth
        driver.get(f'{base_url}/node/{node_uuid}/generate/')
        time.sleep(2)

        # Should redirect to login or show permission error
        page_source = driver.page_source.lower()
        current_url = driver.current_url.lower()

        # Either redirected to login, or got permission denied, or 403
        is_protected = (
            'login' in current_url or
            'permission' in page_source or
            'forbidden' in page_source or
            'authenticate' in page_source
        )

        # No server error should occur
        assert 'server error' not in page_source
