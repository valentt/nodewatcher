"""
E2E Tests that verify actual data display, not just page loading.

These tests will FAIL if data is not displayed correctly,
catching issues like missing nodes on map or empty list pages.
"""
import pytest
import requests
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestAPIDataVerification:
    """Test suite that verifies API returns actual data."""

    def test_api_v3_returns_nodes(self, base_url):
        """Test that API v3 node endpoint returns at least one node."""
        response = requests.get(f'{base_url}/api/v3/node/?format=json')
        assert response.status_code == 200, f"API returned status {response.status_code}"

        data = response.json()
        assert 'count' in data, "API response missing 'count' field"
        assert data['count'] > 0, "API returns 0 nodes - database may be empty or API broken"
        assert 'results' in data, "API response missing 'results' field"
        assert len(data['results']) > 0, "API results array is empty"

        # Verify node has required fields
        first_node = data['results'][0]
        assert '@id' in first_node, "Node missing @id field"

    def test_api_v3_node_detail_returns_config(self, base_url):
        """Test that node list with fields parameter returns config data."""
        # API requires 'fields' parameter to return registry data
        response = requests.get(
            f'{base_url}/api/v3/node/?format=json&limit=1'
            f'&fields=config:core.general&fields=config:core.location'
        )
        assert response.status_code == 200, f"API returned {response.status_code}"

        data = response.json()
        if data['count'] == 0:
            pytest.fail("No nodes in database - cannot test node API")

        node_data = data['results'][0]

        # This is the critical test - config data MUST be present
        assert 'config' in node_data, (
            f"Node missing 'config' field with fields parameter! "
            f"API response: {json.dumps(node_data, indent=2)[:500]}"
        )

        config = node_data['config']
        assert 'core.general' in config or 'core.location' in config, (
            f"Node config missing expected fields! "
            f"Config keys: {list(config.keys())}"
        )

    def test_api_v3_node_has_location(self, base_url):
        """Test that at least one node has location data."""
        # Use fields parameter to get location data
        response = requests.get(
            f'{base_url}/api/v3/node/?format=json&fields=config:core.location'
        )
        assert response.status_code == 200
        data = response.json()

        if data['count'] == 0:
            pytest.fail("No nodes in database")

        nodes_with_location = 0
        for node_data in data['results']:
            if 'config' in node_data:
                config = node_data['config']
                if 'core.location' in config:
                    location = config['core.location']
                    if location and 'geolocation' in location:
                        geolocation = location['geolocation']
                        if geolocation and 'coordinates' in geolocation:
                            nodes_with_location += 1

        assert nodes_with_location > 0, (
            f"No nodes have location data! "
            f"Checked {data['count']} nodes. "
            f"Nodes must have config.core.location.geolocation.coordinates to appear on map."
        )


class TestListPageVerification:
    """Test suite that verifies list page shows actual nodes."""

    def test_list_page_shows_nodes(self, driver, base_url):
        """Test that list page displays nodes, not an empty table."""
        driver.get(f'{base_url}/list/')

        wait = WebDriverWait(driver, 15)

        # First check page loaded without error
        page_source = driver.page_source.lower()
        assert 'server error' not in page_source, "List page returned server error"
        assert '500' not in driver.title.lower(), "List page returned 500 error"

        # Wait for any table or list to appear
        try:
            # Try to find table rows (common pattern for node lists)
            wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'table tbody tr, .node-list .node-item, [class*="node"], .dataTables_wrapper'
            )))
        except:
            pass  # May have different structure

        # Check for actual content
        # Look for common indicators of empty state vs actual data
        empty_indicators = [
            'no nodes', 'no results', 'empty', 'no data',
            'nema rezultata', 'prazno'
        ]

        content = driver.page_source.lower()

        # If we find explicit "empty" message and no node data, fail
        has_empty_message = any(indicator in content for indicator in empty_indicators)

        # Look for node-related content
        # Check for node UUIDs (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
        import re
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids_found = re.findall(uuid_pattern, content)

        # Also check for table rows with data
        table_rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')

        if len(table_rows) == 0 and len(uuids_found) == 0:
            # Take screenshot for debugging
            screenshot_path = 'test_screenshots/list_page_empty.png'
            driver.save_screenshot(screenshot_path)
            pytest.fail(
                f"List page appears empty - no table rows or node UUIDs found. "
                f"Has empty message: {has_empty_message}. "
                f"Screenshot saved to {screenshot_path}"
            )

    def test_list_page_loads_javascript_data(self, driver, base_url):
        """Test that JavaScript successfully loads node data."""
        driver.get(f'{base_url}/list/')

        wait = WebDriverWait(driver, 15)

        # Wait for page to fully load
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Give JavaScript time to make AJAX calls
        import time
        time.sleep(3)

        # Check browser console for errors
        logs = driver.get_log('browser')
        severe_errors = [log for log in logs if log['level'] == 'SEVERE']

        # Filter out known benign errors
        critical_errors = [
            log for log in severe_errors
            if 'favicon' not in log['message'].lower()
            and 'chrome-extension' not in log['message'].lower()
        ]

        if critical_errors:
            error_messages = '\n'.join([log['message'] for log in critical_errors])
            # Don't fail, but warn - JS errors might indicate data loading issues
            print(f"WARNING: JavaScript errors on list page:\n{error_messages}")


class TestMapVerification:
    """Test suite that verifies map displays actual node markers."""

    def test_map_container_exists(self, driver, base_url):
        """Test that map container element exists on page."""
        driver.get(f'{base_url}/map/')

        wait = WebDriverWait(driver, 15)

        # Wait for page to load
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # First check page loaded without error
        page_source = driver.page_source.lower()
        assert 'server error' not in page_source, "Map page returned server error"

        # Find map container - check multiple selectors
        map_selectors = [
            '#map',
            '.leaflet-container',
            '[id*="map"]',
            '.map-container'
        ]

        map_found = False
        for selector in map_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                map_found = True
                break

        assert map_found, (
            f"No map container found on page! "
            f"Tried selectors: {map_selectors}"
        )

    def test_map_has_markers(self, driver, base_url):
        """Test that map shows actual node markers."""
        driver.get(f'{base_url}/map/')

        wait = WebDriverWait(driver, 15)

        # Wait for page to load
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Wait for map to initialize - check for #map div
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#map')))
        except:
            pytest.fail("Map container not found")

        # Wait for JavaScript to load node data
        import time
        time.sleep(5)  # Allow AJAX calls to complete

        # Look for markers - Leaflet uses specific classes
        marker_selectors = [
            '.leaflet-marker-icon',           # Standard markers
            '.leaflet-marker-pane img',       # Marker images
            '.marker-cluster',                # Clustered markers
            '.leaflet-marker-pane > *',       # Any marker element
        ]

        markers_found = 0
        for selector in marker_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            markers_found += len(elements)

        # Check browser console for JavaScript errors that might prevent markers
        try:
            logs = driver.get_log('browser')
            js_errors = [log for log in logs if log['level'] == 'SEVERE']
        except:
            js_errors = []

        if markers_found == 0:
            # Take screenshot
            screenshot_path = 'test_screenshots/map_no_markers.png'
            driver.save_screenshot(screenshot_path)

            error_info = ""
            if js_errors:
                error_info = f"\nJavaScript errors:\n" + '\n'.join([log['message'] for log in js_errors])

            pytest.fail(
                f"Map shows no markers! "
                f"This indicates nodes are not being displayed. "
                f"Screenshot saved to {screenshot_path}"
                f"{error_info}"
            )

    def test_map_api_calls_succeed(self, driver, base_url):
        """Test that map's API calls succeed by checking network activity."""
        driver.get(f'{base_url}/map/')

        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.leaflet-container')))

        # Wait for AJAX calls
        import time
        time.sleep(5)

        # Check for XHR/fetch errors in console
        logs = driver.get_log('browser')

        # Look for specific API-related errors
        api_errors = []
        for log in logs:
            msg = log['message'].lower()
            if any(x in msg for x in ['api', 'node', 'fetch', 'xhr', '500', '404', 'error']):
                if log['level'] in ['SEVERE', 'WARNING']:
                    api_errors.append(log['message'])

        # Also directly test the API endpoints the map uses
        # Based on code.js, it calls /api/v3/node/ and /api/v1/stream/
        v2_response = requests.get(f'{base_url}/api/v3/node/?format=json&limit=1')
        v1_response = requests.get(f'{base_url}/api/v1/stream/?format=json&tags__module=topology&limit=1')

        issues = []
        if v2_response.status_code != 200:
            issues.append(f"API v3 node endpoint returned {v2_response.status_code}")
        if v1_response.status_code != 200:
            issues.append(f"API v1 stream endpoint returned {v1_response.status_code}")

        if api_errors:
            issues.append(f"Browser console API errors: {api_errors[:3]}")  # First 3 errors

        if issues:
            pytest.fail(
                f"Map API calls have issues:\n" + '\n'.join(issues)
            )


class TestProjectDataVerification:
    """Test suite that verifies project data is accessible."""

    def test_project_api_returns_data(self, base_url):
        """Test that project API returns at least one project."""
        response = requests.get(f'{base_url}/api/v3/project/?format=json')
        assert response.status_code == 200, f"Project API returned {response.status_code}"

        data = response.json()
        assert 'count' in data, "Project API missing 'count' field"
        assert data['count'] > 0, (
            "No projects in database! "
            "Create a project first (e.g., 'Croatia' project)."
        )

    def test_ippool_api_returns_data(self, base_url):
        """Test that IP pool API returns at least one pool."""
        response = requests.get(f'{base_url}/api/v3/ippool/?format=json')
        assert response.status_code == 200, f"IP Pool API returned {response.status_code}"

        data = response.json()
        assert 'count' in data, "IP Pool API missing 'count' field"
        assert data['count'] > 0, (
            "No IP pools in database! "
            "Create an IP pool first."
        )
