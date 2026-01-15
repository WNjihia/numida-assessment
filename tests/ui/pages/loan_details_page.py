"""
Loan Details Page Object
"""

from pages.base_page import BasePage


class LoanDetailsPage(BasePage):
    PAGE_HEADING = 'h2:has-text("Loan Details")'
    LOAN_AMOUNT_INPUT = 'input#loanAmount'
    LOAN_TERM_SELECT = 'select#loanTerm'
    PURPOSE_INPUT = 'textarea#purpose'
    SUBMIT_BTN = '.btn-primary:has-text("Submit Application")'
    BACK_BTN = '.btn-secondary:has-text("Back")'
    ERROR_MESSAGE = '.error-message'

    def assert_page_loaded(self):
        self.wait_for(self.PAGE_HEADING)
        assert self.is_visible(self.PAGE_HEADING), "Loan Details page not loaded"

    def is_displayed(self):
        return self.is_visible(self.PAGE_HEADING)
    
    def enter_loan_amount(self, amount):
        self.fill(self.LOAN_AMOUNT_INPUT, str(amount))
        return self
    
    def select_loan_term(self, term):
        self.page.locator(self.LOAN_TERM_SELECT).select_option(term)
        return self
    
    def enter_purpose(self, purpose):
        self.fill(self.PURPOSE_INPUT, purpose)
        return self
    
    def click_submit(self):
        self.click(self.SUBMIT_BTN)
        return self
    
    def fill_form(self, amount, term, purpose):
        self.enter_loan_amount(amount)
        self.select_loan_term(term)
        self.enter_purpose(purpose)
        return self
    
    def submit(self, amount, term, purpose):
        self.fill_form(amount, term, purpose)
        self.click_submit()
        return self
    
    def get_error_message(self):
        if self.is_visible(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    def assert_error_msg(self, error_msg):
        self.wait_for(self.ERROR_MESSAGE)
        actual_txt = self.get_error_message()
        assert error_msg == actual_txt, f"Expected '{error_msg}' but got '{actual_txt}'"
