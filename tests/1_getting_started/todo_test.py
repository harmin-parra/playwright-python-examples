import pytest
from playwright.sync_api import Page, expect
import time


@pytest.fixture(autouse=True)
def goto(page: Page):
    page.goto("https://example.cypress.io/todo")
    yield
    time.sleep(0)  # If you want to add a pause at the end of each test.


def test_1(page: Page):
    """ displays two todo items by default """
    tasks = page.locator(".todo-list li")
    expect(tasks).to_have_count(2)
    expect(tasks.first).to_have_text("Pay electric bill")
    expect(tasks.last).to_have_text("Walk the dog")


def test_2(page: Page):
    """ can add new todo items """
    new = page.locator('[data-test="new-todo"]')
    new.fill("Feed the cat")
    new.press("Enter")
    tasks = page.locator(".todo-list li")
    expect(tasks).to_have_count(3)
    expect(tasks.last).to_have_text("Feed the cat")


@pytest.fixture
def item_checked(page: Page):
    """ Get a checked task """
    page.locator("li").filter(has_text="Pay electric bill").get_by_role("checkbox").check()


def test_3(page: Page, item_checked):
    """ can check off an item as completed """
    expect(page.locator("li").filter(has_text="Pay electric bill")).to_have_class("completed")


def test_4(page: Page, item_checked):
    """ can filter for uncompleted tasks """
    page.get_by_role("link", name="Active").click()
    tasks = page.locator(".todo-list li")
    expect(tasks).to_have_count(1)
    expect(tasks.first).to_have_text("Walk the dog")


def test_5(page: Page, item_checked):
    """ can filter for completed tasks """
    page.get_by_role("link", name="Completed").click()
    tasks = page.locator(".todo-list li")
    expect(tasks).to_have_count(1)
    expect(tasks.first).to_have_text("Pay electric bill")


def test_6(page: Page, item_checked):
    """ can delete all completed tasks """
    page.get_by_role("button", name="Clear completed").click()
    tasks = page.locator(".todo-list li")
    expect(tasks).to_have_count(1)
    expect(tasks).not_to_have_text("Pay electric bill")
