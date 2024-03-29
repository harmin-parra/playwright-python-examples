import json
import os
import pytest
import time
from playwright.sync_api import Page, Route, Playwright


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/files")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1_fixture(page: Page):
    """ load a fixture """
    def handle_route(route: Route):
        f = open(f"tests{os.sep}fixtures{os.sep}example.json")
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


def test_2_readfile():
    """ read file contents """
    f = open(f"tests{os.sep}fixtures{os.sep}example.json")
    example1 = json.load(f)
    f.close()
    example2 = json.loads("""
        {
            "body": "Fixtures are a great way to mock data for responses to routes",
            "email": "hello@cypress.io",
            "name": "Using fixtures to represent data"
        }""")
    assert json.dumps(example1, sort_keys=True) == json.dumps(example2, sort_keys=True)


def test_4_writefile(page: Page, playwright: Playwright):
    """ write to a file """
    # using goto()
    response = page.goto("https://jsonplaceholder.cypress.io/users").body()
    f = open(f"tests{os.sep}fixtures{os.sep}users.json", "wb")
    f.write(response)
    f.close()
    f = open(f"tests{os.sep}fixtures{os.sep}users.json")
    users = json.load(f)
    f.close()
    assert 'name' in users[0]

    # using APIResponse
    context = playwright.request.new_context(base_url="https://jsonplaceholder.cypress.io")
    response = context.get("/users")
    assert response.ok
    assert response.status == 200
    f = open(f"tests{os.sep}fixtures{os.sep}users.json", "wb")
    f.write(response.body())


def test_5_upload(page: Page):
    """ upload a file """
    # with page.expect_file_chooser() as fc:
    #     page.locator("xxx").click()
    # fc.value.set_files("/path/to/file")
    pytest.skip("https://example.cypress.io/commands/files doesn't have a file input")


def test_6_download(page: Page):
    """ download a file """
    # with page.expect_download() as download_info:
    #     page.locator("xxx").click()
    # download_info.value.save_as("/path/to/file")
    pytest.skip("https://example.cypress.io/commands/files doesn't have a file to download")
