import pytest
import time
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/connectors")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ .each() - iterate over an array of elements """
    elms = page.locator(".connectors-its-ul>li")
    for i in range(elms.count()):
        elms.nth(i).evaluate(
            "elem => $(elem).each(function(index) {"
            "        console.log(index + ':' + $(this).text());"
            "    }"
            ")"
        )


def test_2(page: Page):
    """ get properties on the current subject """
    assert page.locator(".connectors-its-ul>li").count() > 2


def test_3(page: Page):
    """ .evaluate() - invoke a function on the current subject """
    elem = page.locator(".connectors-div")
    expect(elem).not_to_be_visible()
    elem.evaluate("elem => $(elem).show()")
    # elem.evaluate("elem => { elem.style.display = 'initial' }")
    expect(elem).to_be_visible()


def test_4():
    """ spread an array as individual args to function """
    arr = ['foo', 'bar', 'baz']

    def func(foo, bar, baz):
        assert foo == 'foo'
        assert bar == 'bar'
        assert baz == 'baz'
    func(*arr)


def test_5(page: Page):
    """ invokes a callback function with the current subject """
    elms = page.locator(".connectors-list > li")
    assert elms.count() == 3, "3 items"
    expect(elms.nth(0)).to_contain_text("Walk the dog")
    expect(elms.nth(1)).to_contain_text("Feed the cat")
    expect(elms.nth(2)).to_contain_text("Write JavaScript")


def test_6():
    """ yields the returned value to the next command """
    def num(x):
        assert x == 1
        return 2
    assert num(1) == 2


def test_7():
    """ yields the original subject without return """
    def num(x):
        assert x == 1
    num(1)


def test_8():
    """ yields the value yielded by the last Cypress command inside """
    def num(x):
        assert x == 1
        return 2
    assert num(1) == 2
