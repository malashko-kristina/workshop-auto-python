import re
from playwright.sync_api import Page, expect
import allure


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        with allure.step(f"Navigating to URL: {url}"):
            self.page.goto(url)

    def press_on_enter_keyboard_button(self):
        with allure.step("Press 'Enter' on the physical keyboard"):
            self.page.keyboard.press('Enter')

    def check_url(self, expected_url, equal=True):
        if equal:
            with allure.step(f"The expected URL contains {expected_url}"):
                expect(self.page).to_have_url(expected_url)
        else:
            with allure.step(f"The expected URL contains {expected_url}"):
                pattern = f".*{re.escape(expected_url)}.*"
                expect(self.page).to_have_url(re.compile(pattern))

    def wait_for_url_change(self, expected_url):
        with allure.step(f"Waiting for the URL to change to {expected_url}"):
            self.page.wait_for_url(expected_url, timeout=30000)

    def check_box(self, selector):
        with allure.step("Checking the checkbox"):
            self.page.check(selector)

    def wait_for_page_load(self):
        with allure.step("Waiting for the page to load"):
            self.page.wait_for_load_state("load", timeout=90000)

    def click_button(self, selector):
        with allure.step(f"Click on the element: {selector}"):
            self.wait_for_selector(selector)
            self.page.click(selector)

    def is_element_visible(self, selector):
        with allure.step(f"Checking the visibility of the element: {selector}"):
            expect(self.page.locator(selector)).to_be_visible()

    def is_button_active(self, selector):
        with allure.step(f"Checking if the button is enabled: {selector}"):
            expect(self.page.locator(selector)).to_be_enabled(timeout=30000)

    def input_text(self, selector, text):
        with allure.step(f"Entering test '{text}' into the element: {selector}"):
            self.page.fill(selector, text)

    def input_filtred_text(self, selector, text):
        with allure.step(f"Entering the test 'FILTRED' into {selector}"):
            self.page.fill(selector, text)

    def wait_for_selector(self, selector):
        with allure.step(f"Waiting for the selector to appear: {selector}"):
            self.page.wait_for_selector(
                selector, state='visible', timeout=100000)

    def wait_for_disappear_selector(self, selector):
        with allure.step(f"Waiting for the selector to appear: {selector}"):
            self.page.wait_for_selector(selector, state='detached')

    def assert_text_present_on_page(self, text):
        with allure.step(f"Checking for the presence of text '{text}' on the page"):
            expect(self.page).to_have_text(text)

    def assert_text_in_element(self, selector, text):
        with allure.step(f"Checking for the presence of text '{text}' in the element: {selector}"):
            expect(self.page.locator(selector)).to_have_text(text)

    def assert_element_attribute(self, selector, attribute, value):
        with allure.step(f"Checking the value '{value}' of the {attribute} attribute of the element: {selector}"):
            expect(self.page.locator(selector)
                   ).to_have_attribute(attribute, value)

    def assert_element_hidden(self, selector):
        with allure.step(f"Checking that the element {selector} is hidden"):
            expect(self.page.locator(selector)).to_be_hidden()

    def s(self, selector):
        with allure.step("Checking that the error text is red"):
            error_element = self.page.locator(selector)
            color = error_element.evaluate(
                '(element) => window.getComputedStyle(element).color')
            return color == "rgb(238, 68, 80)"
