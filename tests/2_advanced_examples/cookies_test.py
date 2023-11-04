import pytest
import time
from playwright.sync_api import Page, Route, expect

url = "https://example.cypress.io/commands/cookies"


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/cookies")
    page.context.clear_cookies()
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ cookies() - get a browser cookies """
    page.locator("#getCookie .set-a-cookie").click()
    assert page.context.cookies()[0]['name'] == "token"
    assert page.context.cookies()[0]['value'] == "123ABC"


def test_2(page: Page):
    """ cookies() - get browser cookies for the current domain """
    assert len(page.context.cookies()) == 0
    page.locator("#getCookie .set-a-cookie").click()
    assert len(page.context.cookies()) == 1
    assert page.context.cookies()[0]['name'] == "token"
    assert page.context.cookies()[0]['value'] == "123ABC"
    assert page.context.cookies()[0]['httpOnly'] is False
    assert page.context.cookies()[0]['secure'] is False
    assert 'domain' in page.context.cookies()[0]
    assert 'path' in page.context.cookies()[0]


def test_3(page: Page):
    """ cookies() - get all browser cookies """
    assert len(page.context.cookies()) == 0
    page.context.add_cookies([
        {
            "name": "key",
            "value": "value",
            "url": url,
        },
        {
            "name": "key",
            "value": "value",
            "domain": ".example.com",
            "path": "/",
        }
    ])
    assert len(page.context.cookies()) == 2
    assert page.context.cookies()[0]['name'] == 'key'
    assert page.context.cookies()[0]['value'] == 'value'
    assert page.context.cookies()[0]['httpOnly'] is False
    assert page.context.cookies()[0]['secure'] is True
    assert 'domain' in page.context.cookies()[0]
    assert 'path' in page.context.cookies()[0]

    assert page.context.cookies()[1]['name'] == 'key'
    assert page.context.cookies()[1]['value'] == 'value'
    assert page.context.cookies()[1]['httpOnly'] is False
    assert page.context.cookies()[1]['secure'] is False
    assert page.context.cookies()[1]['domain'] == ".example.com"
    assert 'path' in page.context.cookies()[0]


def test_4(page: Page):
    """ add_cookies() - set a browser cookie """
    assert len(page.context.cookies()) == 0
    page.context.add_cookies([
        {
            "name": "foo",
            "value": "bar",
            "url": url,
        },
    ])
    assert page.context.cookies()[0]['name'] == "foo"


def test_5(page: Page):
    """ clear_cookies() - clear a browser cookie by name """
    pytest.skip("Playwright doesn't allow cookie deletion by cookie name")


def test_6(page: Page):
    """ clear_cookies() - clear browser cookies for the current domain """
    assert len(page.context.cookies()) == 0
    page.locator("#getCookie .set-a-cookie").click()
    assert len(page.context.cookies()) == 1
    page.context.clear_cookies()
    assert len(page.context.cookies()) == 0


def test_7(page: Page):
    """ clear_cookies() - clear all browser cookies """
    assert len(page.context.cookies()) == 0
    page.context.add_cookies([
        {
            "name": "key",
            "value": "value",
            "url": url,
        },
        {
            "name": "key",
            "value": "value",
            "domain": ".example.com",
            "path": "/",
        }
    ])
    assert len(page.context.cookies()) == 2
    page.context.clear_cookies()
    assert len(page.context.cookies()) == 0
