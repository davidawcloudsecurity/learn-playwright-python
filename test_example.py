import re
import pytest
from playwright.sync_api import sync_playwright, expect

# & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=C:\temp\chrome_debug_profile 
# python -m pytest test_example.py --url https://google.com

# Configuration
CDP_URL = "http://127.0.0.1:9222"
DEFAULT_URL = "https://playwright.dev/"


def pytest_addoption(parser):
    parser.addoption("--url", action="store", default=DEFAULT_URL, help="Target URL to test")


@pytest.fixture
def target_url(request):
    return request.config.getoption("--url")


def get_browser(p):
    """Connect to existing Chrome on port 9222, otherwise launch new Chrome"""
    try:
        browser = p.chromium.connect_over_cdp(CDP_URL)
        print(f"Connected to existing Chrome on {CDP_URL}")
        return browser, True
    except Exception:
        browser = p.chromium.launch(headless=False, channel="chrome", slow_mo=500)
        print("Launched new Chrome browser")
        return browser, False


def test_open_url(target_url):
    with sync_playwright() as p:
        browser, is_cdp = get_browser(p)
        context = browser.contexts[0] if is_cdp else browser.new_context()
        page = context.new_page()

        page.goto(target_url)
        print(f"Opened: {target_url}")
        print(f"Title: {page.title()}")

        expect(page).not_to_have_title(re.compile("^$"))

        page.close()
        if not is_cdp:
            browser.close()