import pytest
from playwright.sync_api import Page, expect
import time


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/todo")
    yield
    time.sleep(1)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ can add new todo items """
    expect(page.locator(".todo-list li")).to_have_count(2)
    expect(page.locator(".todo-list li").first).to_have_text("Pay electric bill")
    expect(page.locator(".todo-list li").last).to_have_text("Walk the dog")


def test_2(page: Page):
    """ can check off an item as completed """
    page.locator('[data-test="new-todo"]').fill("Feed the cat")
    page.locator('[data-test="new-todo"]').press("Enter")
    expect(page.locator(".todo-list li")).to_have_count(3)
    expect(page.locator(".todo-list li").last).to_have_text("Feed the cat")


@pytest.fixture
def item_checked(page: Page):
    """ Get a checked task """
    page.locator("li").filter(has_text="Pay electric bill").get_by_role("checkbox").check()


def test_3(page: Page, item_checked):
    """ can filter for uncompleted tasks """
    page.get_by_role("link", name="Active").click()
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.locator(".todo-list li").first).to_have_text("Walk the dog")


def test_4(page: Page, item_checked):
    """ can filter for completed tasks """
    page.get_by_role("link", name="Completed").click()
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.locator(".todo-list li").first).to_have_text("Pay electric bill")


def test_5(page: Page, item_checked):
    """ can delete all completed tasks """
    page.get_by_role("button", name="Clear completed").click()
    expect(page.locator(".todo-list li")).to_have_count(1)
    expect(page.locator(".todo-list li")).not_to_have_text("Pay electric bill")
