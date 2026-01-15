"""
Common functionality for all pages
"""

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page, base_url):
        self.page = page
        self.base_url = base_url

    def click(self, element):
        self.page.locator(element).click()

    def fill(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).text_content()
    
    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()
    
    def navigate(self, path: str = ""):
        self.page.goto(f"{self.base_url}{path}")
    
    def wait_for(self, selector: str, timeout: int = 5000):
        self.page.locator(selector).wait_for(state="visible", timeout=timeout)