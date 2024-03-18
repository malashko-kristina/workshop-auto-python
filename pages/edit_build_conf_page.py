import time
import allure
from pages.base_page import BasePage

class BuildConfCopyFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions_button = '#sp_span_btActions'
        self.copy_button = '.menuItem >> text="Copy configuration..."'
        self.new_build_name = '#newBuildTypeName'
        self.new_build_id = '#newBuildTypeExternalId'
        self.new_build_counter = '#newBuildCounter'
        self.copy_build_button = '#copyBuildTypeButton'
        self.copy_build_message = '#unprocessed_buildTypeCopied'
        self.error_message_id = '#error_newBuildTypeExternalId'
        self.cancel_button = '#copyBuildTypeFormDialog > div.modalDialogBody > div.popupSaveButtonsBlock > a'


    def copy_build_conf (self, new_build_conf_id, new_build_conf_name):
        with allure.step("Клик на кнопку actions на странице билд конфигурации"):
            self.actions.wait_for_selector(self.actions_button)
            time.sleep(2)
            self.actions.is_element_present(self.actions_button)
            self.actions.click_button(self.actions_button)
            time.sleep(2)
        with allure.step("Клик на кнопку copy для копирования билд конфигурации"):
            self.actions.wait_for_selector(self.copy_button)
            self.actions.is_element_present(self.copy_button)
            self.actions.click_button(self.copy_button)
            time.sleep(2)
        with allure.step("Добавления нового билд конф name в поле build cond name"):
            time.sleep(2)
            self.actions.input_text(self.new_build_name, new_build_conf_name)
        with allure.step("Добавления нового билд конф id в поле build cond id"):
            self.actions.input_text(self.new_build_id, new_build_conf_id)
            time.sleep(2)
        with allure.step("Клик на кнопку копирования билд конфигурации"):
            self.actions.is_element_present(self.copy_build_button)
            self.actions.click_button(self.copy_build_button)

    def message_after_copy_build_conf(self):
        self.actions.wait_for_selector(self.copy_build_message)
        time.sleep(2)
        self.actions.assert_text_in_element(self.copy_build_message, f'Build configuration has been copied successfully.')

    def error_message_copy_build_conf(self, build_conf_id, first_symbol):
        self.actions.wait_for_selector(self.error_message_id)
        time.sleep(2)
        with allure.step("Проверка отображения текста ошибки"):
            self.actions.assert_text_in_element(self.error_message_id, f'Build configuration or template ID "{build_conf_id}" is invalid: starts with non-letter character \'{first_symbol}\'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters).')
            self.actions.check_error_text_color(self.error_message_id)

    def tap_on_cancel_button(self):
        with allure.step("Клик на кнопку отмены"):
            self.actions.is_element_present(self.cancel_button)
            self.actions.click_button(self.cancel_button)


class BuildConfCopyPage(BasePage):

    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/admin/editBuild.html?id=buildType:{build_conf_id}')
        self.build_conf_copy = BuildConfCopyFragment(page)


    def go_to_edit_build_conf_page(self):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()


    def copy_build_conf(self, new_build_conf_id, new_build_conf_name):
        with allure.step("Переход на страницу редактирования"):
            self.go_to_edit_build_conf_page()
            time.sleep(2)
        with allure.step("Копирование билд конфигурации"):
            self.build_conf_copy.copy_build_conf(new_build_conf_id, new_build_conf_name)
            time.sleep(2)
            self.page_url = f'/admin/editBuild.html?id=buildType:{new_build_conf_id}'
            self.actions.wait_for_url_change(self.page_url)
            time.sleep(2)
        with allure.step("Проверка сообщения об успешном копировании билд конфигурации"):
            self.build_conf_copy.message_after_copy_build_conf()


class BuildConfCopyErrorPage(BasePage):

    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/admin/editBuild.html?id=buildType:{build_conf_id}')
        self.build_conf_copy = BuildConfCopyFragment(page)


    def go_to_edit_build_conf_page(self):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()


    def copy_build_conf_error(self, new_build_conf_id, build_conf_id, first_symbol, new_build_conf_name):
        with allure.step("Переход на страницу редактирования"):
            self.go_to_edit_build_conf_page()
            time.sleep(2)
        with allure.step("Копирование билд конфигурации"):
            self.build_conf_copy.copy_build_conf(new_build_conf_id, new_build_conf_name)
            time.sleep(2)
        with allure.step("Проверка отображения неуспешного копирования билд конфигурации"):
            self.build_conf_copy.error_message_copy_build_conf(build_conf_id, first_symbol)
            time.sleep(2)
        with allure.step("Клик на кнопку отмены копирования билд конфигурации"):
            self.build_conf_copy.tap_on_cancel_button()

class BuildConfDDeleteFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions_button = '#sp_span_btActions'
        self.delete_button = '.menuItem >> text="Delete..."'
        self.delete_build_conf_message = '#message_buildTypeRemoved'


    def delete_build_conf (self):
        with allure.step("Клик на кнопку actions на странице билд конфигурации"):
            self.actions.wait_for_selector(self.actions_button)
            self.actions.click_button(self.actions_button)
            time.sleep(2)
        with allure.step("Клик на кнопку 'OK' в диалоговом окне"):
            self.page.on('dialog', lambda dialog: dialog.accept())
        with allure.step("Клик на кнопку удаления билд конфигурации"):
            self.actions.wait_for_selector(self.delete_button)
            self.actions.click_button(self.delete_button)

            time.sleep(2)

    def message_after_delete_build_conf(self, build_conf_name):
        self.actions.wait_for_selector(self.delete_build_conf_message)
        time.sleep(2)
        with allure.step("Проверка сообщения об удалении билд конфигурации"):
            self.actions.assert_text_in_element(self.delete_build_conf_message, f'Build configuration "{build_conf_name}" has been removed.Please note that build configuration related data (builds history, artifacts and so on) will be cleaned from the database when next clean-up process is started, see clean-up policy configuration.')


class BuildConfDeletePage(BasePage):

    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/admin/editBuild.html?id=buildType:{build_conf_id}')
        self.build_conf_delete = BuildConfDDeleteFragment(page)


    def go_to_edit_build_conf_page(self):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()


    def delete_build_conf(self, project_id, build_conf_name):
        with allure.step("Удаление билд конфигурации"):
            self.build_conf_delete.delete_build_conf()
            self.page_url = f'/admin/editProject.html?projectId={project_id}#buildTypeRemoved'
            self.actions.wait_for_url_change(self.page_url)
            time.sleep(2)
        with allure.step("Проверка сообщения об удалении билд конфигурации"):
            self.build_conf_delete.message_after_delete_build_conf(build_conf_name)

