"""
Personal Details Page Object
"""

from pages.base_page import BasePage


class PersonalDetailsPage(BasePage):
    PAGE_HEADING = 'h2:has-text("Personal Details")'

    def assert_page_loaded(self):
        self.wait_for(self.PAGE_HEADING)
        assert self.is_visible(self.PAGE_HEADING), "Personal Details page not loaded"