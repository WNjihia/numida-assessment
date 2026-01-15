"""
Loan Details Page Object
"""

from pages.base_page import BasePage


class LoanDetailsPage(BasePage):
    PAGE_HEADING = 'h2:has-text("Loan Details")'

    def assert_page_loaded(self):
        self.wait_for(self.PAGE_HEADING)
        assert self.is_visible(self.PAGE_HEADING), "Loan Details page not loaded"