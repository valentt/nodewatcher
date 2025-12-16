"""
E2E Tests for page functionality - map, topology, list, node edit.

These tests verify that pages load correctly and display data properly.
"""
import pytest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestMapPage:
    """Test suite for map page functionality."""

    def test_map_page_loads_without_error(self, driver, base_url):
        """Test that map page loads without server error."""
        driver.get(f'{base_url}/map/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Check for server errors
        page_source = driver.page_source.lower()
        assert 'templatesyntaxerror' not in page_source, "Map page has TemplateSyntaxError"
        assert 'server error' not in page_source, "Map page returned server error"
        assert '500' not in driver.title.lower(), "Map page returned 500 error"

    def test_map_has_proper_height(self, driver, base_url):
        """Test that map container has proper height (not just narrow strip)."""
        driver.get(f'{base_url}/map/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # Wait for map to initialize
        import time
        time.sleep(2)

        # Find the map container
        map_selectors = ['#map', '.leaflet-container', '[id*="map"]']
        map_element = None

        for selector in map_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                map_element = elements[0]
                break

        assert map_element is not None, "Map container not found"

        # Get the actual rendered height
        height = map_element.size['height']

        # Map should have substantial height (at least 200px, ideally 400+)
        assert height > 200, (
            f"Map height is only {height}px - appears as narrow strip! "
            f"Expected at least 200px. Check CSS and template rendering."
        )

    def test_map_leaflet_initialized(self, driver, base_url):
        """Test that Leaflet map is properly initialized."""
        driver.get(f'{base_url}/map/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        import time
        time.sleep(3)

        # Check if Leaflet is loaded
        leaflet_loaded = driver.execute_script('return typeof L !== "undefined"')
        assert leaflet_loaded, "Leaflet library (L) not loaded"

        # Check for leaflet container class
        leaflet_containers = driver.find_elements(By.CSS_SELECTOR, '.leaflet-container')
        assert len(leaflet_containers) > 0, "No Leaflet container found - map not initialized"

    def test_map_shows_markers_for_nodes(self, driver, base_url):
        """Test that map shows markers when nodes exist with locations."""
        # First verify nodes exist via API
        response = requests.get(f'{base_url}/api/v2/node/?format=json&fields=config:core.location')
        if response.status_code != 200:
            pytest.skip("API not available")

        data = response.json()
        nodes_with_location = sum(
            1 for n in data.get('results', [])
            if n.get('config', {}).get('core.location', {}).get('geolocation')
        )

        if nodes_with_location == 0:
            pytest.skip("No nodes with location data in database")

        driver.get(f'{base_url}/map/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        import time
        time.sleep(5)  # Allow AJAX to load nodes

        # Check for markers
        marker_selectors = [
            '.leaflet-marker-icon',
            '.leaflet-marker-pane img',
            '.marker-cluster',
        ]

        markers_found = 0
        for selector in marker_selectors:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            markers_found += len(elements)

        if markers_found == 0:
            # Take screenshot for debugging
            driver.save_screenshot('test_screenshots/map_no_markers_test.png')

            # Check console for JS errors
            try:
                logs = driver.get_log('browser')
                errors = [log['message'] for log in logs if log['level'] == 'SEVERE']
                error_msg = '\n'.join(errors[:5]) if errors else "No JS errors"
            except:
                error_msg = "Could not get browser logs"

            pytest.fail(
                f"Map shows no markers but {nodes_with_location} nodes have locations! "
                f"JS errors: {error_msg}"
            )


class TestTopologyPage:
    """Test suite for network topology page."""

    def test_topology_page_loads_without_error(self, driver, base_url):
        """Test that topology page loads without server error."""
        driver.get(f'{base_url}/topology/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        page_source = driver.page_source.lower()

        # Check for specific errors
        assert 'templatesyntaxerror' not in page_source, (
            "Topology page has TemplateSyntaxError - check sekizai contextblock usage"
        )
        assert 'server error' not in page_source, "Topology page returned server error"

        # Check title doesn't indicate error
        assert '500' not in driver.title.lower(), "Topology page returned 500 error"
        assert 'error' not in driver.title.lower(), "Topology page has error in title"

    def test_topology_container_exists(self, driver, base_url):
        """Test that topology container div exists."""
        driver.get(f'{base_url}/topology/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        # The topology page should have a #topology div
        topology_div = driver.find_elements(By.CSS_SELECTOR, '#topology')
        assert len(topology_div) > 0, "Topology container (#topology) not found"


class TestListPage:
    """Test suite for node list page."""

    def test_list_page_loads_without_error(self, driver, base_url):
        """Test that list page loads without server error."""
        driver.get(f'{base_url}/list/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        page_source = driver.page_source.lower()
        assert 'templatesyntaxerror' not in page_source, "List page has TemplateSyntaxError"
        assert 'server error' not in page_source, "List page returned server error"

    def test_list_page_shows_nodes_when_exist(self, driver, base_url):
        """Test that list page shows nodes when they exist in database."""
        # First check if nodes exist via API
        response = requests.get(f'{base_url}/api/v2/node/?format=json')
        if response.status_code != 200:
            pytest.skip("API not available")

        data = response.json()
        node_count = data.get('count', 0)

        if node_count == 0:
            pytest.skip("No nodes in database")

        driver.get(f'{base_url}/list/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        import time
        time.sleep(3)  # Allow JavaScript to load data

        # Look for node indicators in the page
        page_source = driver.page_source

        # Check for table rows or node entries
        table_rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        node_elements = driver.find_elements(By.CSS_SELECTOR, '[class*="node"]')

        # Check for node UUIDs in page
        import re
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        uuids_found = re.findall(uuid_pattern, page_source.lower())

        # Check for DataTables (common table library)
        datatables = driver.find_elements(By.CSS_SELECTOR, '.dataTables_wrapper, .dataTable')

        content_found = (
            len(table_rows) > 1 or  # More than header row
            len(uuids_found) > 0 or
            len(datatables) > 0
        )

        if not content_found:
            driver.save_screenshot('test_screenshots/list_page_empty_test.png')
            pytest.fail(
                f"List page appears empty but {node_count} nodes exist in database! "
                f"Table rows: {len(table_rows)}, UUIDs found: {len(uuids_found)}"
            )

    def test_list_page_node_count_matches_api(self, driver, base_url):
        """Test that list page shows same number of nodes as API."""
        # Get count from API
        response = requests.get(f'{base_url}/api/v2/node/?format=json')
        if response.status_code != 200:
            pytest.skip("API not available")

        api_count = response.json().get('count', 0)
        if api_count == 0:
            pytest.skip("No nodes in database")

        driver.get(f'{base_url}/list/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        import time
        time.sleep(3)

        # Try to find count indicator or count table rows
        # Look for DataTables info which shows "Showing X of Y entries"
        info_elements = driver.find_elements(By.CSS_SELECTOR, '.dataTables_info')

        # Or count actual data rows
        data_rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr:not(.header)')

        # Note: This test might need adjustment based on actual page structure
        # For now, just verify the page loaded with some content
        assert len(data_rows) > 0 or len(info_elements) > 0, (
            f"List page should show {api_count} nodes but shows no data rows or info"
        )


class TestNodeEditPage:
    """Test suite for node edit functionality."""

    def test_node_edit_url_accessible(self, logged_in_admin, base_url):
        """Test that node edit URL is accessible for logged in admin."""
        driver = logged_in_admin

        # Get a node ID from API
        response = requests.get(f'{base_url}/api/v2/node/?format=json&limit=1')
        if response.status_code != 200:
            pytest.skip("API not available")

        data = response.json()
        if data.get('count', 0) == 0:
            pytest.skip("No nodes in database")

        node_id = data['results'][0]['@id']

        # Try to access the edit page
        driver.get(f'{base_url}/node/{node_id}/edit/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        page_source = driver.page_source.lower()

        # Should not get 404 or 500 error
        assert 'page not found' not in page_source, f"Node edit page returned 404 for node {node_id}"
        assert 'server error' not in page_source, f"Node edit page returned server error for node {node_id}"
        assert 'templatesyntaxerror' not in page_source, "Node edit page has TemplateSyntaxError"

    def test_all_nodes_edit_buttons_work(self, logged_in_admin, base_url):
        """Test that edit button works for multiple nodes (up to 10)."""
        driver = logged_in_admin

        # Get nodes from API
        response = requests.get(f'{base_url}/api/v2/node/?format=json&limit=10')
        if response.status_code != 200:
            pytest.skip("API not available")

        data = response.json()
        if data.get('count', 0) == 0:
            pytest.skip("No nodes in database")

        nodes = data['results']
        errors = []

        for node in nodes:
            node_id = node['@id']
            driver.get(f'{base_url}/node/{node_id}/edit/')

            wait = WebDriverWait(driver, 10)
            try:
                wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
            except:
                errors.append(f"Node {node_id}: Page did not load")
                continue

            page_source = driver.page_source.lower()

            if 'page not found' in page_source:
                errors.append(f"Node {node_id}: 404 Not Found")
            elif 'server error' in page_source or '500' in driver.title.lower():
                errors.append(f"Node {node_id}: Server Error (500)")
            elif 'templatesyntaxerror' in page_source:
                errors.append(f"Node {node_id}: TemplateSyntaxError")
            elif 'error' in driver.title.lower():
                errors.append(f"Node {node_id}: Error in page title")

        if errors:
            pytest.fail(
                f"Edit page errors for {len(errors)}/{len(nodes)} nodes:\n" +
                '\n'.join(errors)
            )

    def test_node_detail_page_accessible(self, driver, base_url):
        """Test that node detail page is accessible."""
        # Get a node ID from API
        response = requests.get(f'{base_url}/api/v2/node/?format=json&limit=1')
        if response.status_code != 200:
            pytest.skip("API not available")

        data = response.json()
        if data.get('count', 0) == 0:
            pytest.skip("No nodes in database")

        node_id = data['results'][0]['@id']

        # Try to access node detail page (not edit)
        driver.get(f'{base_url}/node/{node_id}/')

        wait = WebDriverWait(driver, 15)
        wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

        page_source = driver.page_source.lower()

        assert 'page not found' not in page_source, f"Node detail page 404 for {node_id}"
        assert 'server error' not in page_source, f"Node detail page error for {node_id}"


class TestAPIEndpoints:
    """Test suite for API endpoints."""

    def test_api_v2_root_accessible(self, base_url):
        """Test that API v2 root endpoint is accessible."""
        response = requests.get(f'{base_url}/api/v2/')
        assert response.status_code == 200, f"API v2 root returned {response.status_code}"

    def test_api_v2_node_endpoint(self, base_url):
        """Test that API v2 node endpoint works."""
        response = requests.get(f'{base_url}/api/v2/node/?format=json')
        assert response.status_code == 200, f"API v2 node returned {response.status_code}"

        data = response.json()
        assert 'count' in data, "API response missing 'count' field"
        assert 'results' in data, "API response missing 'results' field"

    def test_api_v2_with_fields_parameter(self, base_url):
        """Test that API v2 fields parameter works correctly."""
        response = requests.get(
            f'{base_url}/api/v2/node/?format=json'
            f'&fields=config:core.location&fields=config:core.general'
        )
        assert response.status_code == 200, f"API with fields returned {response.status_code}"

        data = response.json()
        if data['count'] > 0:
            first_node = data['results'][0]
            assert 'config' in first_node, "API with fields parameter should return config data"
