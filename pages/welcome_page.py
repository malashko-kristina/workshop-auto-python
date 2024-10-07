import allure
from pages.base_page import BasePage


class CreateTheFirstProjectFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.welcome_text = '.ring-global-font'
        self.create_button_selector = 'a[data-test="create-project"]'

    def click_create_project_button(self):
        with allure.step('Click on the button to create a project'):
            self.actions.is_element_visible(self.create_button_selector)
            self.actions.click_button(self.create_button_selector)

    def check_text_is_visible(self):
        with allure.step('Check text visibility'):
            self.actions.wait_for_selector(self.welcome_text)
            self.actions.is_element_visible(self.welcome_text)
            self.actions.assert_text_in_element(self.welcome_text,
                                                "Welcome to TeamCity")


class CreateTheFirstProjectPage(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.create_the_first_project = CreateTheFirstProjectFragment(page)
        self.page_url = "/favorite/projects"

    def tap_on_create_first_project(self):
        with allure.step('Check the current page'):
            self.actions.check_url(self.page_url, equal=False)
        with allure.step('Check the welcome text'):
            self.create_the_first_project.check_text_is_visible()
        with allure.step('Go to the project creation page'):
            self.create_the_first_project.click_create_project_button()
