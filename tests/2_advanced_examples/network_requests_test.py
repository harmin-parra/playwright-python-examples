import json
import pytest
import requests
import time
from playwright.sync_api import Page, Route, expect, Playwright


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/commands/network-requests")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


@pytest.fixture(scope="module")
def api_request_context(playwright: Playwright):
    request_context = playwright.request.new_context(base_url="https://jsonplaceholder.cypress.io")
    yield request_context
    request_context.dispose()


def test_1a_request(api_request_context):
    """ make an XHR request """
    # Using Playwright
    request = api_request_context.get("/comments")
    assert request.ok
    assert hasattr(request, "headers")
    assert len(request.body().decode()) > 500

    # Using Python 'requests' module
    response = requests.get("https://jsonplaceholder.cypress.io/comments")
    assert response.status_code == 200
    assert hasattr(response, 'headers')
    assert hasattr(response, 'elapsed')
    assert len(response.text) > 500


def test_1b_request(api_request_context):
    """ requests - pass result to the second request """
    # Using Playwright
    response = api_request_context.get("/users?_limit=1")
    assert response.ok
    user = json.loads(response.body().decode())[0]
    assert isinstance(user['id'], int)
    response = api_request_context.post(
        url="/posts",
        data={
            'userId': user['id'],
            'title': 'Cypress Test Runner',
            'body': 'Fast, easy and reliable testing for anything that runs in a browser.',
        })
    assert response.ok
    response = json.loads(response.body().decode())
    assert 'title' in response and response['title'] == 'Cypress Test Runner'
    assert isinstance(response['id'], int)
    assert response['id'] > 100
    assert isinstance(response['userId'], int)
    assert int(response['userId']) == user['id']

    # Using Python 'requests' module
    response = requests.get("https://jsonplaceholder.cypress.io/users?_limit=1")
    user = json.loads(response.text)[0]
    assert isinstance(user['id'], int)
    response = requests.post(
        url="https://jsonplaceholder.cypress.io/posts",
        data={
            'userId': user['id'],
            'title': 'Cypress Test Runner',
            'body': 'Fast, easy and reliable testing for anything that runs in a browser.',
        }
    )
    assert response.status_code == 201
    response = json.loads(response.text)
    assert 'title' in response and response['title'] == 'Cypress Test Runner'
    assert isinstance(response['id'], int)
    assert response['id'] > 100
    assert isinstance(response['userId'], str) and response['userId'].isnumeric()
    assert int(response['userId']) == user['id']


def test_2_intercept(page: Page):
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


def test_3(api_request_context):
    """ request with query parameters """
    # Using Playwright
    response = api_request_context.get(
        url="/comments",
        params={'postId': 1, 'id': 3}
    )
    comment = json.loads(response.text())[0]
    assert 'postId' in comment
    assert comment['postId'] == 1
    assert 'id' in comment
    assert comment['id'] == 3

    # Using Python 'requests' module
    response = requests.get(
        url="https://jsonplaceholder.cypress.io/comments",
        params={'postId': 1, 'id': 3}
    )
    comment = json.loads(response.text)[0]
    assert 'postId' in comment
    assert comment['postId'] == 1
    assert 'id' in comment
    assert comment['id'] == 3
