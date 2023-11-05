import pytest
import time
from urllib.parse import urlparse
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/location")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ get the current URL hash """
    res = urlparse(page.url)
    assert res.fragment == ''


def test_2(page: Page):
    """ get window.location """
    res = urlparse(page.url)
    assert res.fragment == ''
    assert res.geturl() == "https://example.cypress.io/commands/location"
    assert res.hostname == "example.cypress.io"
    assert res.path == "/commands/location"
    assert res.port is None
    assert res.scheme == "https"


def test_3(page: Page):
    """ get the current URL """
    assert page.url == "https://example.cypress.io/commands/location"
