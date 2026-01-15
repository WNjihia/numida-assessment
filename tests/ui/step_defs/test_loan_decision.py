"""
Step definitions for decision feature.
"""
from pytest_bdd import scenarios, given, when, then, parsers


scenarios('../features/loan_decision.feature')


@given("I am a new applicant")
def new_applicant(login_page, test_phone, valid_otp):
    login_page.login(test_phone, valid_otp)


@when(parsers.parse('I complete the application with loan amount "{amount}"'))
def complete_application_with_amount(
    personal_details_page,
    loan_details_page,
    valid_personal_details,
    valid_loan_details,
    amount
):

    personal_details_page.assert_page_loaded()
    personal_details_page.submit(
        valid_personal_details["full_name"],
        valid_personal_details["national_id"],
        valid_personal_details["email"],
        valid_personal_details["date_of_birth"]
    )
    
    loan_details_page.assert_page_loaded()
    loan_details_page.submit(
        amount,
        str(valid_loan_details["loan_term"]),
        valid_loan_details["purpose"]
    )


@given("I have submitted a loan application")
def submitted_application(
    login_page, personal_details_page, loan_details_page, loan_decision_page, test_phone, valid_otp, valid_personal_details, valid_loan_details):

    login_page.login(test_phone, valid_otp)
    personal_details_page.assert_page_loaded()

    personal_details_page.submit(
        valid_personal_details["full_name"],
        valid_personal_details["national_id"],
        valid_personal_details["email"],
        valid_personal_details["date_of_birth"]
    )
    loan_details_page.assert_page_loaded()
    
    loan_details_page.assert_page_loaded()
    loan_details_page.submit(
        str(valid_loan_details["loan_amount"]),
        str(valid_loan_details["loan_term"]),
        valid_loan_details["purpose"]
    )
    
    loan_decision_page.assert_page_loaded()


@when(parsers.parse('I complete the application with date of birth "{dob}"'))
def complete_application_as_senior(
    personal_details_page,
    loan_details_page,
    valid_personal_details,
    valid_loan_details,
    dob
):
    # Personal details with custom DOB
    personal_details_page.assert_page_loaded()
    personal_details_page.submit(
        valid_personal_details["full_name"],
        valid_personal_details["national_id"],
        valid_personal_details["email"],
        dob
    )
    
    # Loan details
    loan_details_page.assert_page_loaded()
    loan_details_page.submit(
        str(valid_loan_details["loan_amount"]),
        str(valid_loan_details["loan_term"]),
        valid_loan_details["purpose"]
    )


@when("I click logout")
def click_logout(loan_decision_page):
    loan_decision_page.click_logout()


@then("I should see the application decision page")
def see_loan_decision_page(loan_decision_page):
    loan_decision_page.assert_page_loaded()


@then(parsers.parse('the status should be "{status}"'))
def verify_status(loan_decision_page, status):
    actual_status = loan_decision_page.get_status()
    assert actual_status == status.lower(), f"Expected '{status}', got '{actual_status}'"


@then("I should see a congratulations message")
def see_congratulations(loan_decision_page):
    assert loan_decision_page.is_visible(loan_decision_page.CONGRATULATIONS_MSG)


@then(parsers.parse('I should see applicant name "{name}"'))
def see_applicant_name(loan_decision_page, name):
    actual_name = loan_decision_page.get_applicant_name()
    assert actual_name == name, f"Expected '{name}', got '{actual_name}'"


@then(parsers.parse('I should see loan amount "{amount}"'))
def see_loan_amount(loan_decision_page, amount):
    actual_amount = loan_decision_page.get_loan_amount()
    assert actual_amount == amount, f"Expected '{amount}', got '{actual_amount}'"


@then(parsers.parse('I should see loan term "{term}"'))
def see_loan_term(loan_decision_page, term):
    actual_term = loan_decision_page.get_loan_term()
    assert actual_term == term, f"Expected '{term}', got '{actual_term}'"


@then("I should see the login page")
def see_login_page(login_page):
    login_page.wait_for(login_page.START_APPLICATION_BTN)
    assert login_page.is_visible(login_page.START_APPLICATION_BTN)