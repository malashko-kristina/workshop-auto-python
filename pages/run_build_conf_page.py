import time
import allure
from pages.base_page import BasePage

class SideBarListBuildConfFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.create_build_conf_from_url_selector = "a.tabs:has-text('Build Steps')"

    def click_create_steps_build_conf(self):
        with allure.step('Выбор создания шагов для билд конфигурации'):
            self.actions.click_button(self.create_build_conf_from_url_selector)

    def is_build_steps_active(self):
        with allure.step('Проверка активности кнопки создания шагов для билд конфигурации'):
            return self.actions.is_element_present(self.create_build_conf_from_url_selector)


class BreadCrumbsWrapperRunBuildConf(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.run_build_conf_selector = "button.btn_mini"

    def click_run_build_conf(self):
        with allure.step('Запуск билд кофигурации'):
            self.actions.click_button(self.run_build_conf_selector)

    def is_run_build_active(self):
        with allure.step('Проверка активности кнопки запуска билд конфигурации'):
            return self.actions.is_element_present(self.run_build_conf_selector)


class BuildConfRunPage(BasePage):
    def __init__(self, page, project_id, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/admin/editBuildTypeVcsRoots.html?init=1&id=buildType:{build_conf_id}&cameFromUrl=%2Fadmin%2FeditProject.html%3Finit%3D1%26projectId%3D{project_id}')
        self.run_build_conf_wrapper = BreadCrumbsWrapperRunBuildConf(page)
        self.create_steps_build_conf_bar = SideBarListBuildConfFragment(page)

    def go_to_creation_build_conf_page(self):
        with allure.step("Переход на страницу запуска билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load(timeout=10000)

    def run_build_conf(self, build_conf_id, project_id):
        self.run_build_conf_wrapper.click_run_build_conf()
        time.sleep(2)
        self.page_url = f'/admin/editBuildTypeVcsRoots.html?init=1&id=buildType:{build_conf_id}&cameFromUrl=%2Fadmin%2FeditProject.html%3Finit%3D1%26projectId%3D{project_id}'
        self.actions.wait_for_url_change(self.page_url)

    def tap_on_add_build_steps(self, build_conf_id):
        with allure.step("Клик на кнопку перехода на страницу создания шагов к билд конфигурации"):
            self.create_steps_build_conf_bar.click_create_steps_build_conf()
            self.page_url = f"/admin/editBuildRunners.html?id=buildType:{build_conf_id}"





