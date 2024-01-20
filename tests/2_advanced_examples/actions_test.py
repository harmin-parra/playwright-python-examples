import pytest
import re
import time
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/actions")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_01_type(page: Page):
    """ fill()/press() - type into a DOM element """
    email = page.locator(".action-email")
    email.fill("fake@email.com")
    expect(email).to_have_value("fake@email.com")
    assert email.evaluate("elem => elem.value") == "fake@email.com"
    assert email.evaluate("elem => $(elem).val()") == "fake@email.com"
    # Special characters
    email.press("ArrowLeft")
    email.press("ArrowRight")
    email.press("ArrowUp")
    email.press("ArrowDown")
    # Key modifiers
    email.press("Alt+a")
    email.press("Shift+A")
    email.press("Control+a")
    email.press("Delete")
    email.press_sequentially("slow.typing@email.com")
    expect(email).to_have_value("slow.typing@email.com")
    # Playwright can't force typing into a disabled input or textarea.
    # page.locator(".action-disabled").fill("disabled error checking", force=True)
    # expect(page.locator("textarea")).to_have_value("disabled error checking")


def test_02_focus(page: Page):
    """ focus() - focus on a DOM element """
    page.locator(".action-focus").focus()
    expect(page.locator(".action-focus")).to_be_focused()
    # Playwright doesn't have prev() locator
    expect(page.get_by_text("Password")).to_have_attribute("style", "color: orange;")


def test_03_blur(page: Page):
    """ blur() - blur off a DOM element """
    elem = page.locator(".action-blur")
    elem.type("About to blur")
    elem.blur()
    expect(elem).to_have_class(re.compile("error"))
    # Playwright doesn't have prev() locator
    expect(page.get_by_text("Full Name")).to_have_attribute("style", "color: red;")


def test_04_clear(page: Page):
    """ clear() - clears an input or textarea element """
    elem = page.locator(".action-clear")
    elem.fill("Clear this text")
    expect(elem).to_have_value("Clear this text")
    elem.clear()
    expect(elem).to_have_value('')


def test_05_submit(page: Page):
    """ click() - submit a form """
    page.locator(".action-form").locator("[type='text']").fill("HALFOFF")
    page.get_by_role("button", name="Submit").click()
    # Playwright doesn't have next() locator
    expect(page.get_by_text("Your form has been submitted!", exact=True)).to_be_visible()


def test_06_click(page: Page):
    """ click() - click on a DOM element """
    page.locator(".action-btn").click()
    canvas = page.locator("#action-canvas")
    # Playwright doesn't have keyword positions: 'topLeft', 'top', 'topRight', 'left', etc.
    canvas.click(position={'x': 80, 'y': 75})
    canvas.click(position={'x': 175, 'y': 75})
    canvas.click(position={'x': 80, 'y': 165})
    canvas.click(position={'x': 100, 'y': 185})
    canvas.click(position={'x': 125, 'y': 190})
    canvas.click(position={'x': 150, 'y': 185})
    canvas.click(position={'x': 170, 'y': 165})
    buttons = page.locator('.action-labels>.label')
    for i in range(buttons.count()):
        buttons.nth(i).click()
    page.locator(".action-opacity>.btn").click(force=True)


def test_07_dblclick(page: Page):
    """ dblclick() - double click on a DOM element """
    page.locator(".action-div").dblclick()
    expect(page.locator(".action-div")).not_to_be_visible()
    expect(page.locator(".action-input-hidden")).to_be_visible()


def test_08_rightclick(page: Page):
    """ rightclick() - right click on a DOM element """
    page.locator(".rightclick-action-div").click(button="right")
    expect(page.locator(".rightclick-action-div")).not_to_be_visible()
    expect(page.locator(".rightclick-action-input-hidden")).to_be_visible()


def test_09_check(page: Page):
    """ check() - check a checkbox or radio element """
    boxes = page.locator(".action-checkboxes [type='checkbox'] :enabled")
    for i in range(boxes.count()):
        boxes.nth(i).check()
        expect(boxes.nth(i)).to_be_checked()

    radios = page.locator(".action-radios [type='radio'] :enabled")
    for i in range(radios.count()):
        radios.nth(i).check()
        expect(radios.nth(i)).to_be_checked()

    radio = page.locator('.action-radios').locator("[value='radio1']")
    radio.check()
    expect(radio).to_be_checked()

    boxes = page.locator(".action-multiple-checkboxes")
    box1 = boxes.locator("[value='checkbox1']")
    box2 = boxes.locator("[value='checkbox2']")
    box1.check()
    box2.check()
    expect(box1).to_be_checked()
    expect(box2).to_be_checked()

    # Playwright can't force clicking a disabled checkbox
    # box = page.locator(".action-checkboxes [disabled]")
    # box = page.locator(".action-checkboxes :disabled")
    # box.check(force=True)
    # expect(box).to_be_checked()

    # Playwright can't force clicking a disabled radio button
    # radio = page.locator(".action-radios").locator("xpath=//input[@type='radio' and @value='radio3']")
    # radio = page.locator(".action-radios").locator("[value='radio3']")
    # radio.check(force=True)
    # expect(radio).to_be_checked()


def test_10_uncheck(page: Page):
    """ uncheck() - uncheck a checkbox element """
    boxes = page.locator(".action-check > :not(.disabled) [type='checkbox']")
    for i in range(boxes.count()):
        boxes.nth(i).uncheck()
        expect(boxes.nth(i)).not_to_be_checked()

    boxes = page.locator(".action-check")

    # box1 = page.locator(".action-check [type='checkbox'][value='checkbox1']")
    box1 = boxes.locator("[type='checkbox'][value='checkbox1']")
    box1.check()
    expect(box1).to_be_checked()
    box1.uncheck()
    expect(box1).not_to_be_checked()

    box1 = boxes.locator("[value='checkbox1']")
    box3 = boxes.locator("[value='checkbox3']")
    box1.check()
    box3.check()
    expect(box1).to_be_checked()
    expect(box3).to_be_checked()
    box1.uncheck()
    box3.uncheck()
    expect(box1).not_to_be_checked()
    expect(box3).not_to_be_checked()

    # Playwright cant force uncheck a checked disabled checkbox
    # box = page.locator(".action-check [disabled]")
    # box.uncheck(force=True)
    # expect(box).not_to_be_checked()


def test_11_select(page: Page):
    """ select() - select an option in a <select> element """
    select1 = page.locator(".action-select")
    expect(select1).to_have_value("--Select a fruit--")

    select1.select_option("apples")
    expect(select1).to_have_value("fr-apples")

    select2 = page.locator(".action-select-multiple")
    select2.select_option(['apples', 'oranges', 'bananas'])
    expect(select2).to_have_values(['fr-apples', 'fr-oranges', 'fr-bananas'])

    select1.select_option("fr-bananas")
    expect(select1).to_have_value("fr-bananas")

    select2.select_option(["fr-apples", "fr-oranges", "fr-bananas"])
    expect(select2).to_have_values(["fr-apples", "fr-oranges", "fr-bananas"])
    # Don't know how to verify 'fr-oranges' is part of selected options in an elegant way with expect()
    expect(select2).to_have_values([re.compile(".*"), re.compile(".*oranges"), re.compile(".*")])
    assert "fr-oranges" in select2.evaluate("elem => $(elem).val()")
    options = select2.evaluate(
        "elem => { "
        "    values = [];"
        "    for (opt of elem.selectedOptions)"
        "        values.push(opt.value);"
        "    return values;"
        "}"
    )
    assert "fr-oranges" in options


def test_12_scrollIntoView(page: Page):
    """ scrollIntoView() - scroll an element into view """
    button = page.locator("#scroll-horizontal button")
    button.scroll_into_view_if_needed()
    expect(button).to_be_visible()

    button = page.locator("#scroll-vertical button")
    button.scroll_into_view_if_needed()
    expect(button).to_be_visible()

    button = page.locator("#scroll-both button")
    button.scroll_into_view_if_needed()
    expect(button).to_be_visible()


def test_13_scrollTo(page: Page):
    """ scrollTo() - scroll the window or element to a position """
    pytest.skip("Playwright doesn't have scrolling built-in functions")


def test_14_trigger(page: Page):
    """ Trigger an event on a DOM element """

    # Set value to the range-input
    elem = page.locator('.trigger-input-range')
    value = 25
    elem.evaluate("(elem, val) => {"
                  "elem.value = val;"
                  "elem.dispatchEvent(new Event('input', { 'bubbles': true }));"
                  "elem.dispatchEvent(new Event('change', { 'bubbles': true }));"
                  "}", value)
    assert int(elem.evaluate("elem => elem.value")) == 25

    # Move range-input slider
    width = elem.evaluate("elem => { return elem.getBoundingClientRect().width }")
    elem.hover(position={'x': 0, 'y': 0})
    page.mouse.down()
    elem.hover(position={'x': width * 25 / 100, 'y': 0})
    page.mouse.up()
    # Assert 24 <= elem.value <= 26
    expect(elem).to_have_value(re.compile(r"^2[456]$"))
    assert 24 <= int(elem.evaluate("elem => elem.value")) <= 25
    assert 24 <= int(elem.evaluate("elem => $(elem).val()")) <= 25
