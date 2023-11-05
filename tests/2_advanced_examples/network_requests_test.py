import json
import pytest
import requests
import time
from playwright.sync_api import Page, Route, expect


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/network-requests")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ make an XHR request """
    r = requests.get("https://jsonplaceholder.cypress.io/comments")
    assert r.status_code == 200
    assert hasattr(r, 'headers')
    assert hasattr(r, 'elapsed')


def test_2(page: Page):
    """ verify XHR request """
    pytest.skip("Same as test_1")


def test_3(page: Page):
    """ request with query parameters """
    r = requests.get(url="https://jsonplaceholder.cypress.io/comments", params={'postId': 1, 'id': 3})
    comment = json.loads(r.text)[0]
    assert 'postId' in comment
    assert comment['postId'] == 1
    assert 'id' in comment
    assert comment['id'] == 3


def test_4(page: Page):
    """ requests - pass result to the second request """
    r = requests.get("https://jsonplaceholder.cypress.io/users?_limit=1")
    user = json.loads(r.text)[0]
    assert isinstance(user['id'], int)
    r = requests.post(
        url="https://jsonplaceholder.cypress.io/posts",
        data={
            'userId': user['id'],
            'title': 'Cypress Test Runner',
            'body': 'Fast, easy and reliable testing for anything that runs in a browser.',
        }
    )
    assert r.status_code == 201
    res = json.loads(r.text)
    assert 'title' in res and res['title'] == 'Cypress Test Runner'
    assert isinstance(res['id'], int)
    assert res['id'] > 100
    assert isinstance(res['userId'], str) and res['userId'].isnumeric()
    assert int(res['userId']) == user['id']


def test_5(page: Page):
    """ request() - save response in the shared test context """
    pytest.skip("Same as test_4")


def test_6(page: Page):
    """ route responses to matching requests """
    message = "whoa, this comment does not exist"
    with page.expect_response("**/comments/*") as response_info:
        page.locator(".network-btn").click()
    assert response_info.value.status in (200, 304)
    with page.expect_response("**/comments") as response_info:
        page.locator(".network-post").click()
    assert 'content-type' in response_info.value.headers
    body = json.loads(response_info.value.body().decode())
    assert 'email' in body
    assert body['name'] == "Using POST in cy.intercept()"

    def handle_route(route: Route):
        route.fulfill(
            status=404,
            json={"error": message},
            # body=json.dumps({"error": message}),
            headers={"access-control-allow-origin": "*", "content-type": "application/json"},
        )
    page.route("**/comments/*", handle_route)
    page.locator(".network-put").click()
    expect(page.locator(".network-put-comment")).to_contain_text(message)


'''
    page.route(
        "**/comments/*",
        lambda route: route.fulfill(status=400))
    page.locator(".network-btn").click()
'''
