"""
Browser and Page Fixtures
"""

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.personal_details_page import PersonalDetailsPage


@pytest.fixture
def login_page(page, base_url):
    return LoginPage(page, base_url)


@pytest.fixture
def personal_details_page(page, base_url):
    return PersonalDetailsPage(page, base_url)