"""
Step Definitions for login feature
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers


scenarios('../features/login.feature')


@given("I am on the application homepage")
def navigate_to_homepage(login_page):
    login_page.navigate()


@when("I click start application")
def start_application(login_page):
    login_page.click_start_application()


@when(parsers.parse('I enter phone number "{phone}"'))
def enter_phone(login_page, phone: str):
    login_page.enter_phone(phone)


@when("I click request OTP")
def click_send_otp(login_page):
    login_page.click_send_otp_btn()


@when(parsers.parse('I enter OTP "{otp}"'))
def enter_otp(login_page, otp: str):
    login_page.enter_otp(otp)


@when("I click verify")
def click_verify(login_page):
    login_page.click_verify_btn()


@then("I should see the personal details page")
def see_personal_details(personal_details_page):
    personal_details_page.assert_page_loaded()