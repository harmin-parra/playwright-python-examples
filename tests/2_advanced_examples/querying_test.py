import pytest
import re
import time
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/querying")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ query DOM elements """
    expect(page.locator("#query-btn")).to_contain_text("Button")
    expect(page.locator(".query-btn")).to_contain_text("Button")
    expect(page.locator("#querying .well>button").first).to_contain_text("Button")

    expect(page.locator("[data-test-id='test-example']")).to_have_class("example")
    expect(page.locator("[data-test-id='test-example']")).to_have_attribute("data-test-id", "test-example")
    assert page.locator("[data-test-id='test-example']").get_attribute("data-test-id") == "test-example"
    assert page.locator("[data-test-id='test-example']").evaluate("elem => $(elem).css('position')") == "static"


def test_2(page: Page):
    """ query DOM elements with matching content """
    expect(page.locator(".query-list").get_by_text("bananas")).to_have_class("third")
    expect(page.locator(".query-list").get_by_text(re.compile(r"^b\w+"))).to_have_class("third")
    expect(page.locator(".query-list").get_by_text("apples", exact=True)).to_have_class("first")

    expect(page.locator("#querying ul").first).to_contain_text("oranges")
    expect(page.locator("#querying ul").first).to_have_class("query-list")

    expect(page.locator(".query-button").get_by_role("button", name="Save Form")).to_have_class(re.compile("btn"))


def test_3(page: Page):
    """ query DOM elements within a specific element """
    elem = page.locator(".query-form")
    expect(elem.locator("input").first).to_have_attribute("placeholder", "Email")
    expect(elem.locator("input").first).to_have_attribute("placeholder", "Password")


def test_4(page: Page):
    """ query the root DOM element """
    pytest.skip("Playwright doesn't have a 'root' locator")
