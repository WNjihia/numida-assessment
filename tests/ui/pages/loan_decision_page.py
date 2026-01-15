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

    def assert_page_loaded(self):
        self.wait_for(self.PAGE_HEADING)
        assert self.is_visible(self.PAGE_HEADING), "Decision page not loaded"