import pytest
import time
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/waiting")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1_wait(page: Page):
    page.locator(".wait-input1").fill("Wait 1000ms after typing")
    time.sleep(1)
    page.locator(".wait-input2").fill("Wait 1000ms after typing")
    time.sleep(1)
    page.locator(".wait-input3").fill("Wait 1000ms after typing")
    time.sleep(1)

    with page.expect_response("**/comments/*") as response_info:
        page.locator('.network-btn').click()
    assert response_info.value.status in (200, 304)
    expect(page.locator(".network-comment")).to_contain_text("laudantium enim quasi")
