import json
import pytest
import time
from playwright.sync_api import Page, Route


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/files")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ load a fixture """
    def handle_route(route: Route):
        f = open("fixtures/example.json")
        route.fulfill(
            json=json.load(f),
        )
        f.close()
    page.route("**/comments/*", handle_route)
    with page.expect_response("**/comments/*") as response_info:
        page.locator(".fixture-btn").click()
    res = json.loads(response_info.value.body().decode())
    assert 'name' in res
    assert "Using fixtures to represent data" in res['name']


def test_2():
    """ load a fixture """
    f = open("fixtures/example.json")
    requiredExample = json.load(f)
    f.close()
    otherExample = json.loads("""
        {
            "body": "Fixtures are a great way to mock data for responses to routes",
            "email": "hello@cypress.io",
            "name": "Using fixtures to represent data"
        }""")
    assert json.dumps(requiredExample, sort_keys=True) == json.dumps(otherExample, sort_keys=True)


def test_3():
    """ read file contents """
    pytest.skip("Playwright doesn't have a configFile")


def test_4(page: Page):
    """ write to a file """
    response = page.goto("https://jsonplaceholder.cypress.io/users").body()
    f = open("fixtures/users.json", "wb")
    f.write(response)
    f.close()
    f = open("fixtures/users.json")
    users = json.load(f)
    f.close()
    assert 'name' in users[0]


def test_5(page: Page):
    """ upload a file """
    # with page.expect_file_chooser() as fc:
    #     page.locator("xxx").click()
    # fc.value.set_files("/path/to/file")
    pytest.skip("https://example.cypress.io/commands/files doesn't have a file input")


def test_6(page: Page):
    """ download a file """
    # with page.expect_download() as download_info:
    #     page.locator("xxx").click()
    # download_info.value.save_as("/path/to/file")
    pytest.skip("https://example.cypress.io/commands/files doesn't have a file to download")
