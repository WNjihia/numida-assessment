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
def enter_phone(login_page, phone):
    login_page.enter_phone(phone)


@when("I enter a new phone number")
def enter_new_phone(login_page, test_phone):
    login_page.enter_phone(test_phone)


@when("I click send OTP")
def click_send_otp(login_page):
    login_page.click_send_otp_btn()


@when(parsers.parse('I enter OTP "{otp}"'))
def enter_otp(login_page, otp):
    login_page.enter_otp(otp)


@when("I click verify")
def click_verify(login_page):
    login_page.click_verify_btn()


@when("I click back button")
def click_back_btn(login_page):
    login_page.click_back_btn()


@then("I should see the personal details page")
def assert_personal_details_page_loaded(personal_details_page):
    personal_details_page.assert_page_loaded()


@then(parsers.parse('I should see the error message "{error_msg}"'))
def assert_invalid_phone_error_message(login_page, error_msg):
    login_page.assert_error_msg(error_msg)


@then("I should see the phone input screen")
def assert_phone_input_screen_loaded(login_page):
    login_page.assert_phone_input_screen()