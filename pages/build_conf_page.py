import time
import allure
from pages.base_page import BasePage

class BuildConfDetailsFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.edit_build_button = 'a[title="Edit configuration..."]'


    def go_to_edit_build_conf_page(self):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.actions.is_button_active(self.edit_build_button)
            self.actions.click_button(self.edit_build_button)


class BuildConfDetailsPage(BasePage):

    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/buildConfiguration/{build_conf_id}')
        self.build_conf_details = BuildConfDetailsFragment(page)


    def go_to_creation_build_conf_detailed_page(self):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load(timeout=10000)


    def edit_build_conf(self, build_conf_id):
        with allure.step("Переход на страницу создания билд конфигурации"):
            self.go_to_creation_build_conf_detailed_page()
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.build_conf_details.go_to_edit_build_conf_page()
            self.page_url = f'/admin/editBuild.html?id=buildType:{build_conf_id}'
            self.actions.wait_for_url_change(self.page_url)
