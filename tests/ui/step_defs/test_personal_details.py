"""
Step Definitions for personal details feature
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers


scenarios('../features/personal_details.feature')


@given("I am logged in as a new applicant")
def log_in(login_page, valid_phone, valid_otp):
    login_page.login(valid_phone, valid_otp)


@when("I submit valid personal details")
def submit_valid_details(personal_details_page, valid_personal_details):
    personal_details_page.submit(
        valid_personal_details["full_name"],
        valid_personal_details["national_id"],
        valid_personal_details["email"],
        valid_personal_details["date_of_birth"]
    )


@when(parsers.parse('I enter full name "{name}"'))
def enter_full_name(personal_details_page, name):
    personal_details_page.enter_full_name(name)


@when(parsers.parse('I enter national ID "{national_id}"'))
def enter_national_id(personal_details_page, national_id):
    personal_details_page.enter_national_id(national_id)


@when(parsers.parse('I enter email "{email}"'))
def enter_email(personal_details_page, email):
    personal_details_page.enter_email(email)


@when(parsers.parse('I enter date of birth "{dob}"'))
def enter_dob(personal_details_page, dob):
    personal_details_page.enter_dob(dob)


@when("I click next")
def click_next(personal_details_page):
    personal_details_page.click_next()


@then("I should remain on the personal details page")
def remain_on_personal_details(personal_details_page):
    assert personal_details_page.is_displayed()


@then("I should see the loan details page")
def assert_personal_details_page_loaded(loan_details_page):
    loan_details_page.assert_page_loaded()
