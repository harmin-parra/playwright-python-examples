import pytest
import time
from urllib.parse import urlparse
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io")
    page.locator(".navbar-nav").get_by_text("Commands").click()
    page.locator(".dropdown-menu").get_by_text("Navigation").click()
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ go back or forward in the browser\'s history """
    assert "navigation" in page.url
    page.go_back()
    assert "navigation" not in page.url
    page.go_forward()
    assert "navigation" in page.url


def test_2(page: Page):
    """ reload() - reload the page """
    page.reload()
