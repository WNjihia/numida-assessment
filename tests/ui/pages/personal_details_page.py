"""
Personal Details Page Object
"""

from pages.base_page import BasePage


class PersonalDetailsPage(BasePage):
    PAGE_HEADING = 'h2:has-text("Personal Details")'
    FULL_NAME_INPUT = 'input#fullName'
    NATIONAL_ID_INPUT = 'input#nationalId'
    EMAIL_INPUT = 'input#email'
    DOB_INPUT = 'input#dob'
    ERROR_MSG = '.error-message'
    NEXT_BTN = '.btn-primary:has-text("Next")'

    def assert_page_loaded(self):
        self.wait_for(self.PAGE_HEADING)
        assert self.is_visible(self.PAGE_HEADING), "Personal Details page not loaded"

    def click_next(self):
        self.click(self.NEXT_BTN)
        return self

    def enter_full_name(self, name):
        self.fill(self.FULL_NAME_INPUT, name)
        return self
    
    def enter_national_id(self, national_id):
        self.fill(self.NATIONAL_ID_INPUT, national_id)
        return self
    
    def enter_email(self, email):
        self.fill(self.EMAIL_INPUT, email)
        return self
    
    def enter_dob(self, dob):
        self.fill(self.DOB_INPUT, dob)
        return self
    
    def fill_form(self, full_name, national_id, email, dob):
        self.enter_full_name(full_name)
        self.enter_national_id(national_id)
        self.enter_email(email)
        self.enter_dob(dob)
        return self
    
    def is_displayed(self):
        return self.is_visible(self.PAGE_HEADING)
    
    def submit(self, full_name, national_id, email, dob):
        self.fill_form(full_name, national_id, email, dob)
        self.click_next()
        return self
    
    def get_error_message(self):
        if self.is_visible(self.ERROR_MSG):
            return self.get_text(self.ERROR_MSG)
        return ""
    
    def assert_error_msg(self, error_msg):
        self.wait_for(self.ERROR_MSG)
        actual_txt = self.get_error_message()
        assert error_msg == actual_txt, f"Expected '{error_msg}' but got '{actual_txt}'"