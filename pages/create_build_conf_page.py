import allure
from pages.base_page import BasePage

class MenuListCreateBuildConfFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.create_build_conf_from_url_selector = "a.createOption:has-text('From a repository URL')"
        self.create_build_conf_manually_selector = "a.createOption:has-text(' Manually')"

    def click_create_build_conf_from_url(self):
        with allure.step('Выбор создания билд конфигурации по url'):
            self.actions.click_button(self.create_build_conf_from_url_selector)

    def click_create_build_conf_manually(self):
        with allure.step('Выбор создания билд конфигурации вручную'):
            self.actions.click_button(self.create_build_conf_manually_selector)

    def is_create_from_url_active(self):
        with allure.step('Проверка активности кнопки создания билд конфигурации по url'):
            return self.actions.is_element_visible(self.create_build_conf_from_url_selector)

    def is_create_manually_active(self):
        with allure.step('Проверка активности кнопки создания билд конфигурации вручную'):
            return self.actions.is_element_visible(self.create_build_conf_manually_selector)


class CreateBuildConfFormContainerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.build_conf_name_selector = "input#buildTypeName"
        self.build_conf_id_selector = "input#buildTypeExternalId"
        self.build_conf_description_selector = "input#description"
        self.create_build_conf_button = 'input.btn.btn_primary.submitButton[name="createBuildType"]'
        self.build_name_error = "#error_buildTypeName"
        self.build_id_error = "#error_buildTypeExternalId"

    def input_build_conf_details(self, build_conf_name, build_conf_id, description):
        with allure.step("Ввод данных для создания билд конфигурации"):
            self.actions.wait_for_selector(self.build_conf_name_selector)
            self.actions.input_text(self.build_conf_name_selector, build_conf_name)
            self.actions.input_text(self.build_conf_id_selector, build_conf_id)
            self.actions.input_text(self.build_conf_description_selector, description)

    def click_create_build_conf_button(self):
        with allure.step("Нажатие кнопки создания билд конфигурации"):
            self.actions.is_element_visible(self.create_build_conf_button)
            self.actions.click_button(self.create_build_conf_button)
    def check_error_message_empty_build_name(self):
        with allure.step("Проверка текста ошибки о пустом имени билда"):
            self.actions.wait_for_selector(self.build_name_error)
            self.actions.assert_text_in_element(self.build_name_error, 'Name must not be empty')
            self.actions.check_error_text_color(self.build_name_error)

    def check_error_message_empty_build_id(self):
        with allure.step("Проверка текста ошибки о пустом id билда"):
            self.actions.wait_for_selector(self.build_id_error)
            self.actions.assert_text_in_element(self.build_id_error, 'The ID field must not be empty.')
            self.actions.check_error_text_color(self.build_id_error)

    def check_error_message_invalid_build_id(self, build_conf_id, first_symbol):
        with allure.step("Проверка текста ошибки о пустом невалидном id билда"):
            self.actions.wait_for_selector(self.build_id_error)
            self.actions.assert_text_in_element(self.build_id_error, f'Build configuration or template ID "{build_conf_id}" is invalid: starts with non-letter character \'{first_symbol}\'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters).')
            self.actions.check_error_text_color(self.build_id_error)

    def check_error_message_used_build_name(self, build_conf_name, project_name):
        with allure.step("Проверка текста ошибки о уже используемом имени билда"):
            self.actions.wait_for_selector(self.build_name_error)
            self.actions.assert_text_in_element(self.build_name_error, f'Build configuration with name "{build_conf_name}" already exists in project: "{project_name}"')
            self.actions.check_error_text_color(self.build_name_error)


class BuildConfCreationPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/createObjectMenu.html?projectId={project_id}&showMode=createBuildTypeMenu&cameFromUrl=%2Fadmin%2FeditProject.html%3FprojectId%3DTests')
        self.menu_list_create_build_conf = MenuListCreateBuildConfFragment(page)
        self.create_build_conf_form_container = CreateBuildConfFormContainerFragment(page)

    def go_to_creation_build_conf_page(self):
        with allure.step("Переход на страницу создания билд конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_build_conf(self, build_conf_id, build_conf_name, description):
        self.go_to_creation_build_conf_page()
        with allure.step("Клик на кнопку ручного создания билд конфигурации"):
            self.menu_list_create_build_conf.click_create_build_conf_manually()
        with allure.step("Добавления информации для создания билд конфигурации"):
            self.create_build_conf_form_container.input_build_conf_details(build_conf_name, build_conf_id, description)
        with allure.step("Клик на кнопку создания билд конфигурации"):
            self.create_build_conf_form_container.click_create_build_conf_button()

    def check_url_after_build_create(self, build_conf_id, project_id):
            self.page_url = (f'/admin/editVcsRoot.html?action=addVcsRoot&editingScope=buildType%3A{build_conf_id}&cameFromUrl=%2Fadmin%2FeditBuildTypeVcsRoots.html%3Finit%3D1%26id%3DbuildType%3A{build_conf_id}%26cameFromUrl%3D%252Fadmin%252FeditProject.html%253Finit%253D1%2526projectId%253D{project_id}&cameFromTitle=Version%20Control%20Settings&showSkip=true')
            self.actions.wait_for_url_change(self.page_url)

    def check_error_empty_build_name(self):
        with allure.step("Проверка ошибки создания билд конфигурации из-за пустого поля имени"):
                self.create_build_conf_form_container.check_error_message_empty_build_name()
    def check_error_empty_build_id(self):
        with allure.step("Проверка ошибки создания билд конфигурации из-за пустого поля id"):
            self.create_build_conf_form_container.check_error_message_empty_build_id()
    def check_error_invalid_build_id(self, build_conf_id, first_symbol):
        with allure.step("Проверка ошибки создания билд конфигурации из-за invalid buuld id"):
            self.create_build_conf_form_container.check_error_message_invalid_build_id(build_conf_id, first_symbol)
    def check_error_used_build_id(self, build_conf_name, project_name):
        with allure.step("Проверка ошибки создания билд конфигурации из-за уже используемого поля name"):
            self.create_build_conf_form_container.check_error_message_used_build_name(build_conf_name, project_name)



