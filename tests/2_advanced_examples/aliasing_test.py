import pytest
import re
import time
from playwright.sync_api import Page, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/aliasing")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ variable for a DOM element for later use """
    firstBtn = (page.locator('.as-table').locator('tbody>tr')
                .first.locator('td').first.locator('button'))
    firstBtn.click()
    expect(firstBtn).to_have_class(re.compile(r"\s*btn-success\s*"))
    assert "btn-success" in firstBtn.get_attribute("class").split()
    assert firstBtn.evaluate("elem => $(elem).hasClass('btn-success')")
    expect(firstBtn).to_have_text("Changed")


def test_2(page: Page):
    """ variable for a network event for later use """
    with page.expect_response("**/comments/*") as response_info:
        page.locator(".network-btn").click()
    response = response_info.value
    assert response.status == 200


'''
    page.route(
        "**/comments/*",
        lambda route: route.fulfill(status=400))
    page.locator(".network-btn").click()
    # page.goto("https://example.cypress.io/commands/aliasing")

    def handle(route: Route):
        json = [{"name": "Strawberry", "id": 21}]
        # fulfill the route with the mock data
        route.fulfill(json=json)
'''