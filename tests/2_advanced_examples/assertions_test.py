import pytest
import re
import time
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/assertions")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ expect() - make an assertion about the current subject """
    elem = page.locator(".assertion-table tbody tr").last
    expect(elem).to_have_class("success")
    elem = elem.locator("td").first
    expect(elem).to_have_text("Column content")
    expect(elem).to_contain_text("Column content")
    assert elem.evaluate("elem => elem.innerHTML") == "Column content"
    assert elem.evaluate("elem => elem.tagName").lower() == "td"
    assert elem.evaluate("elem => elem.textContent") == "Column content"
    expect(elem).to_have_text(re.compile("column content", re.IGNORECASE))

    elem = page.locator(".assertion-table tbody tr").last
    elem = elem.get_by_text(re.compile("column content", re.IGNORECASE)).first
    expect(elem).to_be_visible()


def test_2(page: Page):
    """ chain multiple assertions together """
    # Playwright and the Jest 'expect' library don't support assertions chaining
    elem = page.locator(".assertions-link")
    assert "active" in elem.get_attribute("class").split()
    expect(elem).to_have_class(re.compile(r"\bactive\b"))
    expect(elem).to_have_attribute("href", re.compile(".*cypress.io"))


def test_3():
    """ make an assertion about a specified subject """
    # Let's use python assertions
    assert True is True
    obj = {'foo': 'bar'}
    assert obj == obj
    assert obj == {'foo': 'bar'}
    assert re.search("bar$", "FooBar", re.IGNORECASE)


def test_4(page: Page):
    """ pass your own callback function to expect() """
    # Playwright and the Jest 'expect' library don't support custom callback functions to expect()
    elms = page.locator(".assertions-p p")
    values = []
    for i in range(elms.count()):
        values.append(elms.nth(i).text_content())
    assert len(values) == 3, 'has 3 paragraphs'
    assert values == [
        'Some text from first p',
        'More text from second p',
        'And even more text from third p'
    ], "has expected text in each paragraph"


def test_5(page: Page):
    """ assert element's class name using regex """
    elms = page.locator(".docs-header div")
    assert elms.count() == 1
    classes = elms.first.get_attribute("class").split()
    expect(elms.first).to_have_class(re.compile(r"\bheading-.*"))
    expect(elms.first).to_contain_text("Introduction")


def test_6(page: Page):
    """ can throw any error """
    elms = page.locator(".docs-header div")
    if elms.count() != 1:
        raise Exception("Did not find 1 element")

    classes = elms.first.get_attribute("class")
    if re.search(r"\bheading-.*", classes) is None:
        raise Exception(f'Could not find class "heading-" in {classes}')


def test_7(page: Page):
    """ matches unknown text between two elements """
    elem1 = page.locator(".first")
    text1 = elem1.text_content().replace(' ', '').lower()
    elem2 = page.locator(".second")
    text2 = elem2.text_content().replace(' ', '').lower()
    assert text1 == text2


def test_8(page: Page):
    """ assert shape of an object """
    person = {
        'name': 'Joe',
        'age': 20,
    }
    assert isinstance(person, object), "value is an object"


def test_9(page: Page):
    """ retries the function callback until assertions pass """
    # Playwright and Python don't allow asynchronous callbacks in assertions
    elem = page.locator("#random-number")
    expect(elem).to_have_text(re.compile(r"^[0-9]+$"), timeout=10000);
    value = int(elem.text_content())
    assert 1 < value <= 10
