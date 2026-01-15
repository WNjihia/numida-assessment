"""
Step Definitions for personal details feature
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers


scenarios('../features/loan_details.feature')


@given("I am logged in and on the loan details page")
def log_in_and_navigate_to_loan_details(login_page, personal_details_page, loan_details_page, test_phone, valid_otp, valid_personal_details):
    login_page.login(test_phone, valid_otp)
    personal_details_page.assert_page_loaded()
    personal_details_page.submit(
        valid_personal_details["full_name"],
        valid_personal_details["national_id"],
        valid_personal_details["email"],
        valid_personal_details["date_of_birth"]
    )
    loan_details_page.assert_page_loaded()


@when(parsers.parse('I enter loan amount "{amount}"'))
def enter_loan_amount(loan_details_page, amount: str):
    loan_details_page.enter_loan_amount(amount)


@when(parsers.parse('I select loan term "{term}"'))
def select_loan_term(loan_details_page, term: str):
    loan_details_page.select_loan_term(term)


@when(parsers.parse('I enter purpose "{purpose}"'))
def enter_purpose(loan_details_page, purpose: str):
    loan_details_page.enter_purpose(purpose)


@when("I click submit")
def click_submit(loan_details_page):
    loan_details_page.click_submit()


@then("I should see the decision page")
def see_decision_page(loan_decision_page):
    loan_decision_page.assert_page_loaded()


@then("I should remain on the loan details page")
def remain_on_loan_details(loan_details_page):
    assert loan_details_page.is_displayed()


@then(parsers.parse('I should see the error message "{error_msg}"'))
def assert_loan_error_message(loan_details_page, error_msg):
    loan_details_page.assert_error_msg(error_msg)
