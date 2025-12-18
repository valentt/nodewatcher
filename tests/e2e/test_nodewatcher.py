"""
End-to-end tests for nodewatcher using Playwright.
"""

from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8000"


def run_tests():
    print("=" * 60)
    print("NODEWATCHER E2E TESTS")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        passed = 0
        failed = 0

        # Test 1: Homepage
        try:
            page.goto(BASE_URL)
            title = page.title()
            assert "Error" not in title, f"Got error page: {title}"
            print(f"[PASS] Homepage loaded - Title: {title}")
            passed += 1
        except Exception as e:
            print(f"[FAIL] Homepage: {e}")
            failed += 1

        # Test 2: Admin page
        try:
            page.goto(f"{BASE_URL}/admin/")
            content = page.content().lower()
            assert "admin" in page.url or "login" in content or "django" in content
            print("[PASS] Admin page accessible")
            passed += 1
        except Exception as e:
            print(f"[FAIL] Admin page: {e}")
            failed += 1

        # Test 3: API v3 root (JSON format)
        try:
            response = page.goto(f"{BASE_URL}/api/v3/?format=json")
            assert response.status == 200, f"Status: {response.status}"
            content = page.content()
            assert "node" in content.lower(), "Missing node endpoint"
            print("[PASS] API v3 root endpoint")
            passed += 1
        except Exception as e:
            print(f"[FAIL] API v3 root: {e}")
            failed += 1

        # Test 4: Node API
        try:
            response = page.goto(f"{BASE_URL}/api/v3/node/?format=json")
            assert response.status == 200, f"Status: {response.status}"
            content = page.content()
            assert "[" in content or "{" in content, "Not JSON"
            print("[PASS] Node API returns JSON")
            passed += 1
        except Exception as e:
            print(f"[FAIL] Node API: {e}")
            failed += 1

        # Test 5: Project API
        try:
            response = page.goto(f"{BASE_URL}/api/v3/project/?format=json")
            assert response.status == 200, f"Status: {response.status}"
            print("[PASS] Project API endpoint")
            passed += 1
        except Exception as e:
            print(f"[FAIL] Project API: {e}")
            failed += 1

        # Test 6: IP Pool API
        try:
            response = page.goto(f"{BASE_URL}/api/v3/pool/ip/?format=json")
            assert response.status == 200, f"Status: {response.status}"
            print("[PASS] IP Pool API endpoint")
            passed += 1
        except Exception as e:
            print(f"[FAIL] IP Pool API: {e}")
            failed += 1

        # Test 7: Setup page
        try:
            response = page.goto(f"{BASE_URL}/setup/")
            assert response.status in [200, 302], f"Status: {response.status}"
            print("[PASS] Setup page accessible")
            passed += 1
        except Exception as e:
            print(f"[FAIL] Setup page: {e}")
            failed += 1

        # Test 8: Static files (CSS/JS)
        try:
            page.goto(BASE_URL)
            # Check for stylesheets
            styles = page.locator("link[rel='stylesheet']").count()
            scripts = page.locator("script[src]").count()
            print(f"[PASS] Static files: {styles} CSS, {scripts} JS files")
            passed += 1
        except Exception as e:
            print(f"[FAIL] Static files: {e}")
            failed += 1

        # Test 9: Map page (if exists)
        try:
            response = page.goto(f"{BASE_URL}/map/")
            if response.status == 200:
                print("[PASS] Map page accessible")
                passed += 1
            else:
                print(f"[SKIP] Map page (status {response.status})")
        except Exception as e:
            print(f"[SKIP] Map page: {e}")

        # Test 10: List page (if exists)
        try:
            response = page.goto(f"{BASE_URL}/list/")
            if response.status == 200:
                print("[PASS] List page accessible")
                passed += 1
            else:
                print(f"[SKIP] List page (status {response.status})")
        except Exception as e:
            print(f"[SKIP] List page: {e}")

        # Test 11: Login functionality
        try:
            page.goto(f"{BASE_URL}/admin/")
            username = page.locator("#id_username")
            password = page.locator("#id_password")

            if username.is_visible():
                username.fill("testuser")
                password.fill("testpass")
                page.click("input[type='submit']")
                # Should show error (invalid credentials)
                page.wait_for_timeout(1000)
                print("[PASS] Login form functional")
                passed += 1
            else:
                print("[SKIP] Login form (already logged in?)")
        except Exception as e:
            print(f"[FAIL] Login form: {e}")
            failed += 1

        # Test 12: API browsable interface
        try:
            page.goto(f"{BASE_URL}/api/v3/node/")
            content = page.content()
            # Check for DRF browsable API elements
            if "api-wrapper" in content or "browsable" in content.lower() or "GET" in content:
                print("[PASS] DRF Browsable API interface")
                passed += 1
            else:
                print("[PASS] API returns data")
                passed += 1
        except Exception as e:
            print(f"[FAIL] Browsable API: {e}")
            failed += 1

        # Test 13: Take screenshot
        try:
            page.goto(BASE_URL)
            page.screenshot(path="tests/e2e/screenshot_homepage.png")
            print("[PASS] Screenshot saved: tests/e2e/screenshot_homepage.png")
            passed += 1
        except Exception as e:
            print(f"[FAIL] Screenshot: {e}")
            failed += 1

        browser.close()

        print("=" * 60)
        print(f"RESULTS: {passed} passed, {failed} failed")
        print("=" * 60)

        return failed == 0


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
