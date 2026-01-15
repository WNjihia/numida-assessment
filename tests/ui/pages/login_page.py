"""
Page object for the authentication flow (phone number + OTP verification)
"""

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators
    PAGE_HEADING = 'h1:has-text("First-Time Loan Application")'
    START_APPLICATION_BTN = '.btn-primary:has-text("Start Application")'
    PHONE_INPUT = 'input#phone'
    SEND_OTP_BTN = '.btn-primary:has-text("Send OTP")'
    OTP_INPUT = 'input#otp'
    VERIFY_BTN = '.btn-primary:has-text("Verify")'
    BACK_BTN = '.btn-secondary:has-text("Back")'
    ERROR_MSG = '.error-message'
    PHONE_INPUT_SCREEN_HEADING = 'h2:has-text("Enter Your Phone Number")'

    def navigate(self):
        return super().navigate("/")
    
    def click_start_application(self):
        return self.click(self.START_APPLICATION_BTN)
    
    def click_send_otp_btn(self):
        return self.click(self.SEND_OTP_BTN)
    
    def click_verify_btn(self):
        return self.click(self.VERIFY_BTN)
    
    def click_back_btn(self):
        return self.click(self.BACK_BTN)
    
    def enter_phone(self, phone):
        return self.fill(self.PHONE_INPUT, phone)
    
    def enter_otp(self, otp):
        return self.fill(self.OTP_INPUT, otp)
    
    def get_error_message(self):
        if self.is_visible(self.ERROR_MSG):
            return self.get_text(self.ERROR_MSG)
        return ""
    
    def assert_error_msg(self, error_msg):
        self.wait_for(self.ERROR_MSG)
        actual_txt = self.get_error_message()
        assert error_msg == actual_txt, f"Expected '{error_msg}' but got '{actual_txt}'"

    def assert_phone_input_screen(self):
        self.wait_for(self.PHONE_INPUT_SCREEN_HEADING)
        assert self.is_visible(self.PHONE_INPUT_SCREEN_HEADING), "Phone input screen not loaded"

    def login(self, phone, otp):
        """Full login flow"""
        self.navigate()
        self.click_start_application()
        self.enter_phone(phone)
        self.click_send_otp_btn()
        self.enter_otp(otp)
        self.click_verify_btn()
        return self
