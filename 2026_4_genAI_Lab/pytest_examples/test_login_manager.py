from login_manager import authenticate
import pytest

@pytest.fixture
def fixture_authenticate():
    # Set username and password
    username = "admin"
    password = "password"
    return username, password

@pytest.fixture
def fixture_wrong_password():
    username = "admin"
    password = "wrong_password"
    return username, password

@pytest.fixture
def fixture_wrong_username():
    username = "wrong_username"
    password = "password"
    return username, password

#Unit Test
def test_authenticate(fixture_authenticate, fixture_wrong_password, fixture_wrong_username):
    username, password = fixture_authenticate
    assert authenticate(username, password) == True

    username, password = fixture_wrong_password
    assert authenticate(username, password) == False

    username, password = fixture_wrong_username
    assert authenticate(username, password) == False


# UI Test
def test_authenticate_ui(page, fixture_authenticate):
    page.goto("http://localhost:8000/login")

    username, password = fixture_authenticate
    page.get_by_label("Username").fill(username)
    page.get_by_label("Password").fill(password)
    page.get_by_role("button", name="Login").click()


def test_e2e_ticketbooking(page):
    page.goto("http://localhost:8000/login")

    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").fill("password")
    page.get_by_role("button", name="Login").click()

    page.get_by_role("button", name="Choose Itinerary").click()
    page.get_by_role("button", name="Buy Ticket").click()
    page.get_by_role("button", name="Logout").click()
