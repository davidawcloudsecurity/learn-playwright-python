DEFAULT_URL = "https://playwright.dev/"

def pytest_addoption(parser):
    parser.addoption("--url", action="store", default=DEFAULT_URL, help="Target URL to test")