import time
import allure
from pages.base_page import BasePage

class FormNewBuildStepsFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.step_name_selector = "input#buildStepName"
        self.step_id_selector = "input#newRunnerId"
        self.step_custom_script_selector = ".CodeMirror >> textarea"
        self.step_submit_button_selector = "input.btn.btn_primary.submitButton[name='submitButton']"
        self.step_cancel_button_script_selector = "a.cancel"
        self.error_empty_custom_script = ".error.expanded_true"
        self.error_empty_step_id = "#error_newRunnerId"


    def input_step_details(self, step_name, step_id, text):
        with allure.step("Ввод данных для создания шага для билд конфигурации"):
            self.actions.wait_for_selector(self.step_name_selector)
            time.sleep(1)
            self.actions.input_text(self.step_name_selector, step_name)
            time.sleep(1)
            self.actions.input_text(self.step_id_selector, step_id)
            time.sleep(1)
            self.actions.input_text(self.step_custom_script_selector, text)
            time.sleep(1)

    def click_add_new_step(self):
        with allure.step('Нажатия на кнопку добавления шага для билд конфигурации'):
            self.actions.click_button(self.step_submit_button_selector)
    def is_add_new_active(self):
        with allure.step('Проверка активности кнопки добавления шага для билд конфигурации'):
            self.actions.is_button_active(self.step_submit_button_selector)

    def check_error_message_empty_script(self):
        with allure.step('Проверка сообщения об ошибке насчет пустого поля со скриптом command line'):
            self.actions.wait_for_selector(self.error_empty_custom_script)
            self.actions.assert_text_in_element(self.error_empty_custom_script, "Script content must be specified")
            self.actions.check_error_text_color(self.error_empty_step_id)

    def check_error_message_empty_step_id(self):
        with allure.step('Проверка сообщения об ошибке насчет пустого поля с id step'):
            self.actions.wait_for_selector(self.error_empty_step_id)
            self.actions.assert_text_in_element(self.error_empty_step_id, "Build step ID must not be empty.")
            self.actions.check_error_text_color(self.error_empty_step_id)

    def check_error_message_invalid_step_id(self, build_step_id, first_symbol):
        with allure.step('Проверка сообщения об ошибке насчет невалидного поля с id step'):
            self.actions.wait_for_selector(self.error_empty_step_id)
            self.actions.assert_text_in_element(self.error_empty_step_id, f'Build step ID "{build_step_id}" is invalid: starts with non-letter character \'{first_symbol}\'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 80 characters).')
            self.actions.check_error_text_color(self.error_empty_step_id)


class ContentNewBuildStepCommandLineFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.add_command_line_button_selector = "td.SelectBuildRunners__title--Vf:has-text('Command Line')"

    def click_command_line(self):
        with allure.step('Нажатия на кнопку добавления командной строки для билд конфигурации'):
            self.actions.click_button(self.add_command_line_button_selector)

    def is_build_steps_active(self):
        with allure.step('Проверка активности кнопки добавления командной строки для билд конфигурации'):
            return self.actions.is_element_visible(self.add_command_line_button_selector)


class BuildNewStepPage(BasePage):
    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/admin/editRunType.html?id=buildType:{build_conf_id}&runnerId=__NEW_RUNNER__&cameFromUrl=%2Fadmin%2FeditBuildRunners.html%3Fid%3DbuildType%253A{build_conf_id}%26init%3D1&cameFromTitle=')
        self.command_line_add = ContentNewBuildStepCommandLineFragment(page)
        self.add_build_steps = FormNewBuildStepsFragment(page)


    def go_to_build_steps_page(self):
        with allure.step("Переход на страницу для добавления шагов к билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def add_new_build_step(self, step_name,  step_id, text, build_conf_id):
        with allure.step("Выбор command line в качестве добавляемого шага к билд конфигурации"):
            self.command_line_add.is_build_steps_active()
            self.command_line_add.click_command_line()
            time.sleep(1)
        with allure.step("Заполнение полей для добавления command line в качестве шага к билд конфигурации"):
            self.add_build_steps.input_step_details(step_name, step_id, text)
            time.sleep(1)
        with allure.step("Клик на кнопку добавления шага к билд конфигурации"):
            self.add_build_steps.is_add_new_active()
            time.sleep(1)
            self.add_build_steps.click_add_new_step()
            self.page_url = f'/admin/editRunType.html?id=buildType:{build_conf_id}&runnerId=__NEW_RUNNER__&cameFromUrl=%2Fadmin%2FeditBuildRunners.html%3Fid%3DbuildType%253A{build_conf_id}%26init%3D1&cameFromTitle='
            self.actions.wait_for_url_change(self.page_url)


class BuildNewStepErrorPage(BasePage):
    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/admin/editRunType.html?id=buildType:{build_conf_id}&runnerId=__NEW_RUNNER__&cameFromUrl=%2Fadmin%2FeditBuildRunners.html%3Fid%3DbuildType%253A{build_conf_id}%26init%3D1&cameFromTitle=')
        self.command_line_add = ContentNewBuildStepCommandLineFragment(page)
        self.add_build_steps = FormNewBuildStepsFragment(page)


    def go_to_build_steps_page(self):
        with allure.step("Переход на страницу для добавления шагов к билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def add_new_build_step_empty_script(self, step_name,  step_id, text):
        with allure.step("Выбор command line в качестве добавляемого шага к билд конфигурации"):
            self.command_line_add.is_build_steps_active()
            self.command_line_add.click_command_line()
            time.sleep(1)
        with allure.step("Заполнение полей для добавления command line в качестве шага к билд конфигурации"):
            self.add_build_steps.input_step_details(step_name, step_id, text)
            time.sleep(1)
            self.add_build_steps.is_add_new_active()
        with allure.step("Клик на кнопку добавления шага к билд конфигурации"):
            self.add_build_steps.click_add_new_step()
        with allure.step("Проверка сообщения об ошибке о пустом скрипте command line"):
            self.add_build_steps.check_error_message_empty_script()

    def add_new_build_step_empty_step_id(self, step_name,  step_id, text):
        with allure.step("Заполнение полей для добавления command line в качестве шага к билд конфигурации"):
            self.add_build_steps.input_step_details(step_name, step_id, text)
            time.sleep(1)
            self.add_build_steps.is_add_new_active()
        with allure.step("Клик на кнопку добавления шага к билд конфигурации"):
            self.add_build_steps.click_add_new_step()
        with allure.step("Проверка сообщения об ошибке о пустом step id"):
            self.add_build_steps.check_error_message_empty_step_id()

    def add_new_build_step_invalid_step_id(self, step_name,  step_id, text, build_step_id, first_symbol):
        with allure.step("Заполнение полей для добавления command line в качестве шага к билд конфигурации"):
            self.add_build_steps.input_step_details(step_name, step_id, text)
            time.sleep(1)
            self.add_build_steps.is_add_new_active()
        with allure.step("Клик на кнопку добавления шага к билд конфигурации"):
            self.add_build_steps.click_add_new_step()
        with allure.step("Проверка сообщения об ошибке о невалидном step id"):
            self.add_build_steps.check_error_message_invalid_step_id(build_step_id, first_symbol)

    def add_new_build_step_with_invalid_script(self, step_name,  step_id, text):
        with allure.step("Заполнение полей для добавления command line в качестве шага к билд конфигурации (скрипт написан некорректно)"):
            self.add_build_steps.input_step_details(step_name, step_id, text)
            time.sleep(1)
            self.add_build_steps.is_add_new_active()
            time.sleep(1)
        with allure.step("Клик на кнопку добавления шага к билд конфигурации"):
            self.add_build_steps.click_add_new_step()
            self.actions.wait_for_page_load()







