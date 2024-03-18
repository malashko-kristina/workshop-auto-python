import time
import allure
from pages.base_page import BasePage

class StepAddMessageFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.step_add_message_selector = "div#unprocessed_buildRunnerSettingsUpdated"

    def check_text_in_selector(self):
        with allure.step('Проверка наличия текста на странице'):
            self.actions.assert_text_in_element(self.step_add_message_selector,"Build step settings updated.")

class BreadCrumbsWrapperRunBuildConfWithStep(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.run_build_conf_with_step_selector = "#breadcrumbsWrapper > div.quickLinks > div:nth-child(1) > span > button:nth-child(1)"

    def click_run_build_conf(self):
        with allure.step('Запуск билд кофигурации с шагом'):
            self.actions.click_button(self.run_build_conf_with_step_selector)

    def is_run_build_active(self):
        with allure.step('Проверка активности кнопки запуска билд конфигурации'):
            return self.actions.is_element_present(self.run_build_conf_with_step_selector)


class RunBuildWithStep(BasePage):
    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/admin/editBuildRunners.html?id=buildType:{build_conf_id}')
        self.success_message = StepAddMessageFragment(page)
        self.run_build_with_step = BreadCrumbsWrapperRunBuildConfWithStep(page)


    def go_to_build_steps_page(self):
        with allure.step("Переход на страницу с отображением шагов к билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def run_build_conf_with_step(self, build_conf_id):
        with allure.step("Проверка текста на странице об успешном добавлении шагов к билд конфигурации"):
            self.success_message.check_text_in_selector()
        with allure.step("Клик по кнопке запуска билда"):
            self.run_build_with_step.is_run_build_active()
            self.run_build_with_step.click_run_build_conf()
            time.sleep(2)
            self.page_url = f'/admin/editBuildRunners.html?id=buildType:{build_conf_id}'
            self.actions.wait_for_url_change(self.page_url)

    def run_build_conf_with_invalid_step(self):
        with allure.step("Проверка текста на странице об успешном добавлении шагов к билд конфигурации"):
            self.success_message.check_text_in_selector()
        with allure.step("Клик по кнопке запуска билда с невалидным шагом"):
            self.run_build_with_step.is_run_build_active()
            self.run_build_with_step.click_run_build_conf()





