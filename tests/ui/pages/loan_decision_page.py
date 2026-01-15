"""
Loan Decision Page Object
"""

from pages.base_page import BasePage


class LoanDecisionPage(BasePage):
    PAGE_HEADING = 'h2:has-text("Application Decision")'
    STATUS_BADGE = '.status-badge'
    APPLICANT_NAME = '.summary-item:has-text("Applicant")'
    LOAN_AMOUNT = '.summary-item:has-text("Loan Amount")'
    LOAN_TERM = '.summary-item:has-text("Loan Term")'
    SUBMITTED_DATE = '.summary-item:has-text("Submitted")'
    LOGOUT_BTN = 'button:has-text("Logout")'
    CONGRATULATIONS_MSG = '.decision-message'

    def assert_page_loaded(self):
        self.wait_for(self.PAGE_HEADING)
        assert self.is_visible(self.PAGE_HEADING), "Decision page not loaded"

    def get_status(self):
        return self.get_text(self.STATUS_BADGE).lower()

    def get_applicant_name(self):
        text = self.get_text(self.APPLICANT_NAME)
        return text.replace("Applicant:", "").strip()

    def get_loan_amount(self):
        text = self.get_text(self.LOAN_AMOUNT)
        return text.replace("Loan Amount:", "").strip()

    def get_loan_term(self):
        text = self.get_text(self.LOAN_TERM)
        return text.replace("Loan Term:", "").strip()

    def click_logout(self):
        self.click(self.LOGOUT_BTN)