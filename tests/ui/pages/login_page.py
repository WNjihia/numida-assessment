"""
Page object for the authentication flow (phone number + OTP verification)
"""

from pages.base_page import BasePage


class LoginPage(BasePage):
    # Locators
    START_APPLICATION_BTN = '.btn-primary:has-text("Start Application")'
    PHONE_FIELD = 'input#phone'
    SEND_OTP_BTN = '.btn-primary:has-text("Send OTP")'
    OTP_FIELD = 'input#otp'
    VERIFY_BTN = '.btn-primary:has-text("Verify")'
    BACK_BTN = '.btn-primary:has-text("Back")'

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
        return self.fill(self.PHONE_FIELD, phone)
    
    def enter_otp(self, otp):
        return self.fill(self.OTP_FIELD, otp)