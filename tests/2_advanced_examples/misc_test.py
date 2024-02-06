import os
import platform
import pytest
import subprocess
import time
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/misc")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1_end(page: Page):
    """ end the command chain """
    pytest.skip("Playwright doesn't have an end() command")


def test_2_exec(page: Page):
    """ execute a system command """
    p = subprocess.run(["echo", "Jane Lane"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = p.stdout.decode()
    assert "Jane Lane" in output

    if platform.system() == "win32":
        p = subprocess.run(["print", __file__], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.run(["cat", __file__], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error = p.stderr.decode()
    assert error == ''


def test_3_focused(page: Page):
    """ get the DOM element that has focus """
    page.locator(".misc-form #name").click()
    expect(page.locator(":focus")).to_have_attribute("id", "name")
    expect(page.locator("*:focus")).to_have_attribute("id", "name")

    page.locator(".misc-form #description").click()
    expect(page.locator(":focus")).to_have_attribute("id", "description")


def test_4_screenshot(page: Page):
    """ screenshot() - take a screenshot """
    page.screenshot(path=f"screenshots{os.sep}screenshot-1.png")

    """ screenshot() - change default config of screenshots """
    page.screenshot(path=f"screenshots{os.sep}screenshot-2.png",
                    clip={'x': 0, 'y': 0, 'width': 200, 'height': 300},
                    mask=[page.locator("#end")])


def test_5_wrap(page: Page):
    """ wrap an object """
    pytest.skip("Playwright doesn't have an wrap() command")
