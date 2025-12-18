# Nodewatcher E2E Selenium Tests

Automated end-to-end tests for the nodewatcher application using Selenium WebDriver.

## Prerequisites

1. Python 3.8+
2. Chrome or Firefox browser
3. Running nodewatcher instance (localhost:8000 or configured URL)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Tests can be configured via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `NODEWATCHER_URL` | `http://localhost:8000` | Base URL of nodewatcher |
| `NODEWATCHER_ADMIN_USER` | `admin` | Admin username |
| `NODEWATCHER_ADMIN_PASS` | `admin` | Admin password |
| `SELENIUM_HEADLESS` | `true` | Run in headless mode |
| `SELENIUM_BROWSER` | `chrome` | Browser to use (chrome/firefox) |
| `SELENIUM_IMPLICIT_WAIT` | `10` | Implicit wait timeout (seconds) |
| `SCREENSHOT_DIR` | `test_screenshots` | Directory for failure screenshots |

## Running Tests

### Run all tests
```bash
pytest
```

### Run with visible browser (non-headless)
```bash
SELENIUM_HEADLESS=false pytest
```

### Run specific test file
```bash
pytest test_01_admin_login.py
```

### Run specific test class
```bash
pytest test_02_project_creation.py::TestProjectCreation
```

### Run with HTML report
```bash
pytest --html=report.html
```

### Run tests in parallel
```bash
pytest -n 4  # Requires pytest-xdist
```

## Test Structure

- `test_01_admin_login.py` - Admin login and basic site access tests
- `test_02_project_creation.py` - Project creation (Croatia) tests
- `test_03_ip_pool_creation.py` - IP pool creation and assignment tests
- `test_04_node_creation.py` - Node creation and management tests

## Test Order

Tests are numbered to run in order since some tests depend on data created by previous tests:
1. Login tests verify authentication works
2. Project tests create the "Croatia" project
3. IP pool tests create pools and associate with project
4. Node tests create nodes in the project

## Creating an Admin User

Before running tests, ensure an admin user exists:

```bash
docker-compose exec web python manage.py createsuperuser
```

Or via Django shell:
```python
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'admin')
```

## Troubleshooting

### Tests fail with "Chrome not reachable"
Install ChromeDriver or use webdriver-manager:
```python
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
```

### Tests timeout waiting for elements
Increase implicit wait:
```bash
SELENIUM_IMPLICIT_WAIT=20 pytest
```

### Need to debug failing tests
Run with visible browser:
```bash
SELENIUM_HEADLESS=false pytest -x -s test_04_node_creation.py
```
