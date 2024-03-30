import allure
from pages.base_page import BasePage

class BuildConfEditFragment(BasePage):
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
        self.delete_button = '.menuItem >> text="Delete..."'
        self.delete_build_conf_message = '#message_buildTypeRemoved'

    def tap_on_actions_button(self):
        with allure.step("Клик на кнопку actions на странице билд конфигурации"):
            self.actions.wait_for_selector(self.actions_button)
            self.actions.is_element_visible(self.actions_button)
            self.actions.click_button(self.actions_button)

    def tap_on_copy_build_conf (self, new_build_conf_id, new_build_conf_name):
        with allure.step("Клик на кнопку copy для копирования билд конфигурации"):
            self.actions.wait_for_selector(self.copy_button)
            self.actions.is_element_visible(self.copy_button)
            self.actions.click_button(self.copy_button)
        with allure.step("Добавления нового билд конф name в поле build conf name"):
            self.actions.input_text(self.new_build_name, new_build_conf_name)
        with allure.step("Добавления нового билд конф id в поле build conf id"):
            self.actions.input_text(self.new_build_id, new_build_conf_id)
        with allure.step("Клик на кнопку копирования билд конфигурации"):
            self.actions.is_element_visible(self.copy_build_button)
            self.actions.click_button(self.copy_build_button)

    def message_after_copy_build_conf(self):
        self.actions.wait_for_selector(self.copy_build_message)
        self.actions.assert_text_in_element(self.copy_build_message, f'Build configuration has been copied successfully.')

    def error_message_copy_build_conf(self, build_conf_id, first_symbol):
        with allure.step("Проверка отображения текста ошибки при копировании билд конфигурации"):
            self.actions.wait_for_selector(self.error_message_id)
            self.actions.assert_text_in_element(self.error_message_id, f'Build configuration or template ID "{build_conf_id}" is invalid: starts with non-letter character \'{first_symbol}\'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters).')
            self.actions.check_error_text_color(self.error_message_id)

    def message_after_delete_build_conf(self, build_conf_name):
        with allure.step("Проверка сообщения об удалении билд конфигурации"):
            self.actions.wait_for_selector(self.delete_build_conf_message)
            self.actions.assert_text_in_element(self.delete_build_conf_message, f'Build configuration "{build_conf_name}" has been removed.Please note that build configuration related data (builds history, artifacts and so on) will be cleaned from the database when next clean-up process is started, see clean-up policy configuration.')

    def tap_on_cancel_button(self):
        with allure.step("Клик на кнопку отмены"):
            self.actions.is_element_visible(self.cancel_button)
            self.actions.click_button(self.cancel_button)

    def tap_on_delete_build_conf(self, build_conf_name):
        with allure.step("Клик на кнопку 'OK' в диалоговом окне"):
            self.page.on('dialog', lambda dialog: dialog.accept())
        with allure.step("Клик на кнопку удаления билд конфигурации"):
            self.actions.wait_for_selector(self.delete_button)
            self.actions.click_button(self.delete_button)
        with allure.step("Проверка сообщения об удалении билд конфигурации"):
            self.message_after_delete_build_conf(build_conf_name)

    def url_after_build_conf_deleted(self, project_id):
        with allure.step("Проверка url после успешной удаления билд конфигурации"):
            self.page_url = f'/admin/editProject.html?projectId={project_id}#buildTypeRemoved'
            self.actions.wait_for_url_change(self.page_url)

class BuildConfEditPage(BasePage):

    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f'/admin/editBuild.html?id=buildType:{build_conf_id}')
        self.build_conf_edit = BuildConfEditFragment(page)

    def go_to_edit_build_conf_page(self):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def copy_build_conf (self, new_build_conf_id, new_build_conf_name):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.go_to_edit_build_conf_page()
        with allure.step("Клик на кнопку actions, copy на странице билд конфигурации"):
            self.build_conf_edit.tap_on_actions_button()
            self.build_conf_edit.tap_on_copy_build_conf(new_build_conf_id, new_build_conf_name)
    def check_success_message_build_copy(self,  new_build_conf_id):
        with allure.step("Проверка отображения сообщения об успешном копировании билд конфигурации"):
            self.build_conf_edit.message_after_copy_build_conf()
        with allure.step("Проверка загруженной страницы после создания копии билд конфига"):
            self.page_url = f'/admin/editBuild.html?id=buildType:{new_build_conf_id}'
            self.actions.wait_for_url_change(self.page_url)

    def check_error_message_build_copy(self, build_conf_id, first_symbol):
        with allure.step("Проверка отображения сообщения об ошибке при копировании билд конфигурации"):
            self.build_conf_edit.error_message_copy_build_conf(build_conf_id, first_symbol)
        with allure.step("Клик на кнопку отмены копирования билд конфигурации"):
            self.build_conf_edit.tap_on_cancel_button()

    def delete_build_conf(self, build_conf_name, project_id):
        with allure.step("Переход на страницу редактирования билд конфигурации"):
            self.go_to_edit_build_conf_page()
        with allure.step("Клик на кнопку actions на странице билд конфигурации"):
            self.build_conf_edit.tap_on_actions_button()
        with allure.step("Клик на кнопку удаления билд конфигурации"):
            self.build_conf_edit.tap_on_delete_build_conf(build_conf_name)
        with allure.step("Проверка загрузки страницы после успешного удаления билд конфигурации"):
            self.build_conf_edit.url_after_build_conf_deleted(project_id)
        with allure.step("Проверка сообщения об удалении билд конфигурации"):
            self.build_conf_edit.message_after_delete_build_conf(build_conf_name)
