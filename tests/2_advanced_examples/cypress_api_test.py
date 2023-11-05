import os
import platform
import pytest
import time
from importlib.metadata import version
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/cypress-api")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_01(page: Page):
    """ evaluate() - execute a custom command """
    def console(method="log"):
        assert method in ('log', 'info', 'error', 'warn', 'debug', )
        func = "console.method".replace('method', method)
        return "elem => " + func + "('The subject is: ', elem)"
    page.locator("button").evaluate(console("log"))


def test_02():
    """ .debug() - enable or disable debugging """
    pytest.skip("Playwright cannot debug cookies")


def test_03():
    """ Get CPU architecture """
    print(platform.machine())


def test_04(page: Page):
    """ Get and set configuration options """
    print(page.url)


def test_05(page: Page):
    """ to_be_hidden() - determine if a DOM element is hidden """
    hidden = page.locator(".dom-p p.hidden").first
    visible = page.locator(".dom-p p.visible").first

    expect(hidden).to_be_hidden()
    expect(hidden).not_to_be_visible()
    expect(visible).not_to_be_hidden()
    expect(visible).to_be_visible()


def test_06(page: Page):
    """ Get environment variables """
    os.environ['host'] = "veronica.dev.local"
    os.environ['api_server'] = "http://localhost:8888/v1/"
    assert 'host' in os.environ
    assert os.environ['host'] == "veronica.dev.local"
    os.environ['api_server'] = "http://localhost:8888/v2/"
    assert 'api_server' in os.environ
    assert os.environ['api_server'] == "http://localhost:8888/v2/"


def test_07():
    """ Control what is printed to the Command Log """
    pytest.skip("Playwright doesn't have a log API")


def test_08():
    """ Get underlying OS name """
    print(platform.system())


def test_09():
    print(version("playwright"))


def test_10():
    """ Get current spec information """
    print(os.path.basename(__file__))
    print(__file__)
