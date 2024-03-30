import allure
from pages.base_page import BasePage

class MessageProjectCreatedFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.message_created_project_locator = ".successMessage#message_projectCreated"

    def check_text_in_selector(self, project_name):
        with allure.step('Проверка наличия текста на странице'):
            self.actions.wait_for_selector(self.message_created_project_locator)
            self.actions.assert_text_in_element(self.message_created_project_locator,f'Project "{project_name}" has been successfully created. You can now create a build configuration.')


class OptionsProjectCreatedFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions_button = '.popupLink[type="button"] >> text=" Actions "'
        self.go_to_project_page_button = 'a.buildTypeName >> text="Go to project page"'
        self.delete_project_button = '.menuItem a[href="#"][title="Delete project"]'
        self.copy_project_button = 'a[title="Copy project"]'
        self.copy_button = '#copyButton'
        self.after_copy_message = '#message_projectCopied'
        self.after_delete_message = '#message_projectRemoved'
        self.project_id_selector = "input#externalId"
        self.new_project_id = '#newProjectExternalId'
        self.message_error_empty_id = '#error_newProjectExternalId'

    def tap_on_actions_button(self):
        with allure.step("Клик на кнопку actions на странице проекта"):
            self.actions.wait_for_selector(self.actions_button)
            self.actions.is_button_active(self.actions_button)
            self.actions.click_button(self.actions_button)

    def tap_on_delete_project_button(self):
        with allure.step("Клик на кнопку удаления на странице проекта"):
            self.actions.wait_for_selector(self.delete_project_button)
            self.actions.assert_text_in_element(self.delete_project_button, "Delete project...")
            self.actions.click_button(self.delete_project_button)

    def message_delete_project(self):
            self.actions.wait_for_selector(self.after_delete_message)
            # todo self.actions.assert_text_in_element(self.after_delete_message, f'Project "{name}" has been moved to the "config/_trash" directory. All project related data (build history, artifacts, and so on) will be cleaned from the database during the next clean-up. See clean-up policy configuration.You can undo the deletion by moving the "config/_trash/{project_id}.project17024" to the "config/projects/{project_id}" manually')

    def tap_on_copy_project_button(self, project_id):
        with allure.step("Клик на кнопку copy для копирования проекта"):
            self.actions.is_element_visible(self.copy_project_button)
            self.actions.click_button(self.copy_project_button)
            self.actions.wait_for_selector(self.copy_button)
        with allure.step("Добавления нового проджект id в поле project id"):
            self.actions.input_text(self.new_project_id, project_id)
        with allure.step("Клик на кнопку копирования проекта"):
            self.actions.is_element_visible(self.copy_button)
            self.actions.click_button(self.copy_button)

    def success_message_copy_project(self):
        with allure.step("Проверка отображения текста об успешном копировании проекта"):
            self.actions.wait_for_selector(self.after_copy_message)
            self.actions.assert_text_in_element(self.after_copy_message,'Project has been copied successfully. Project name has been changed because another project with the same name already exists. Project-associated settings were copied.')

    def error_message_copy_project_empty_id(self):
        with allure.step("Проверка отображения текста об ошибке копирования проекта (project id пустой)"):
            self.actions.wait_for_selector(self.message_error_empty_id)
            self.actions.assert_text_in_element(self.message_error_empty_id,'Project ID must not be empty.')


class EditProjectPageFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_selector = "input#name"
        self.project_id_selector = "input#externalId"
        self.project_description_selector = "input#description"
        self.project_save_button_selector = '.submitButton[name="submitButton"]'
        self.project_cancel_button_selector = ".cancel"
        self.invalid_id_error = '#errorExternalId'
        self.warning_message ='#changeExternalIdWarning'
        self.message_success = '#message_projectUpdated'
        self.empty_id_copy_error = '#error_newProjectExternalId'

    def input_project_edit_details(self, name, project_id, description):
        with allure.step("Ввод данных для изменения проекта"):
            self.actions.input_text(self.project_name_selector, name)
            self.actions.input_text(self.project_id_selector, project_id)
            self.actions.input_text(self.project_description_selector, description)

    def check_project_name(self, name):
        with allure.step("Проверка имени проекта"):
            self.actions.assert_element_attribute(self.project_name_selector, "value", f"{name}")

    def check_project_id(self, project_id):
        with allure.step("Проверка данных проекта"):
            self.actions.assert_element_attribute(self.project_id_selector, "value", f"{project_id}")

    def check_description(self, description):
        with allure.step("Проверка description проекта"):
            self.actions.assert_element_attribute(self.project_description_selector, "value", f"{description}")

    def click_save_project_edit_button(self):
        with allure.step("Нажатие кнопки изменения созданного проекта"):
            self.actions.is_element_visible(self.project_save_button_selector)
            self.actions.click_button(self.project_save_button_selector)

    def click_cancel_project_edit_button(self):
        with allure.step("Нажатие кнопки отмены изменения созданного проекта"):
            self.actions.is_element_visible(self.project_cancel_button_selector)
            self.actions.click_button(self.project_cancel_button_selector)

    def warning_message_displaying(self):
        with allure.step("Отображение предупреждения после редактирования данных проекта"):
            self.actions.wait_for_selector(self.warning_message)

    def error_message_invalid_project_id_edit(self, project_id):
        with allure.step("Проверка отображения сообщения об ошибке при редактировании проекта (невалидный project id)"):
            self.actions.wait_for_selector(self.invalid_id_error)
            self.actions.assert_text_in_element(self.invalid_id_error, f"Project ID \"{project_id}\" is invalid: starts with non-letter character '{project_id[0]}'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters).")

    def error_message_empty_project_id_copy(self):
        with allure.step("Проверка отображения сообщения об ошибке при копировании проекта (пустой project id)"):
            self.actions.wait_for_selector(self.empty_id_copy_error)
            self.actions.assert_text_in_element(self.empty_id_copy_error, f"Project ID must not be empty.")

    def success_message_edit_saved(self):
        with allure.step("Отображения сообщения об успешном сохранении данных редактирования проекта"):
            self.actions.wait_for_selector(self.message_success)
            self.actions.assert_text_in_element(self.message_success, 'Your changes have been saved.')


class AddBuildConf(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.build_conf_add_button_selector = 'span.addNew:has-text("Create build configuration")'
        self.build_conf_templates_button_selector = 'span.addNew:has-text("Create template")'
        self.subproject_button_selector = 'span.addNew:has-text("Create subproject")'

    def click_on_create_build_cond(self):
        with allure.step("Нажатие кнопки создания билд конфигурации"):
            self.actions.wait_for_selector(self.build_conf_add_button_selector)
            self.actions.is_element_visible(self.build_conf_add_button_selector)
            self.actions.click_button(self.build_conf_add_button_selector)


class EditProjectFormPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.options_drop_down_menu = OptionsProjectCreatedFragment(page)
        self.message_created_project = MessageProjectCreatedFragment(page)
        self.edit_project_page = EditProjectPageFragment(page)
        self.add_build_conf = AddBuildConf(page)

    def go_to_edit_page(self):
        with allure.step("Переход на страницу редактирования проекта"):
            self.actions.navigate(self.page_url)

    def wait_edit_project_url(self):
        with allure.step("Проверка открытия страницы редактирования проекта"):
            self.actions.wait_for_url_change(self.page_url)
    def check_project_url_edit(self):
        with allure.step("Проверка открытия страницы редактирования проекта"):
            self.actions.check_url(self.page_url)

    def check_success_project_creation(self, name, project_id, description):
        with allure.step("Проверка сообщения об успешном создании проекта и данных проекта"):
            self.wait_edit_project_url()
            self.message_created_project.check_text_in_selector(name)
            self.edit_project_page.check_project_name(name)
            self.edit_project_page.check_project_id(project_id)
            self.edit_project_page.check_description(description)

    def add_changes_to_project_data(self, name, project_id, description):
        with allure.step("Ввод изменений полей данных проекта"):
            self.edit_project_page.input_project_edit_details(name, project_id, description)
            self.edit_project_page.click_save_project_edit_button()

    def tap_on_save_changes_button(self):
        with allure.step("Сохранение изменений данных проекта"):
            self.edit_project_page.click_save_project_edit_button()

    def redirect_to_create_build_conf(self, project_id):
        with allure.step("Клик на кнопку создания билд конфигурации"):
            self.add_build_conf.click_on_create_build_cond()
            self.page_url = f"/admin/createObjectMenu.html?projectId={project_id}&showMode=createBuildTypeMenu&cameFromUrl=%2Fadmin%2FeditProject.html%3FprojectId%3D{project_id}"
            self.actions.check_url(self.page_url, equal=False)

    def check_error_message_invalid_project_id_edit(self, project_id):
        with allure.step("Проверка отображения сообщения об ошибке при редактировании проекта (невалидный project id)"):
            self.edit_project_page.error_message_invalid_project_id_edit(project_id)

    def check_warning_message_edit(self):
        with allure.step("Отображение предупреждения после редактирования данных проекта"):
            self.edit_project_page.warning_message_displaying()

    def check_success_message_edit_saved(self):
        with allure.step("Отображения сообщения об успешном сохранении данных редактирования проекта"):
            self.edit_project_page.success_message_edit_saved()

    def check_success_message_project_copy(self):
        with allure.step("Проверка отображения текста об успешном копировании проекта"):
            self.options_drop_down_menu.success_message_copy_project()

    def delete_project(self):
        with allure.step("Удаление проекта"):
            self.options_drop_down_menu.tap_on_actions_button()
            self.options_drop_down_menu.tap_on_delete_project_button()
            self.options_drop_down_menu.message_delete_project()

    def copy_project(self, project_id):
        with allure.step("Копирование проекта"):
            self.options_drop_down_menu.tap_on_actions_button()
            self.options_drop_down_menu.tap_on_copy_project_button(project_id)

    def check_error_message_project_copy(self):
        with allure.step("Отображение сообщения об ошибке при создании копии проекта с пустым id"):
            self.edit_project_page.error_message_empty_project_id_copy()





