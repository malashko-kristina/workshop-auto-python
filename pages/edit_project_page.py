import time
import allure
from pages.base_page import BasePage
from pages.create_project_page import ProjectCreationPage

class MessageProjectCreatedFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.message_created_project_locator = "#message_projectCreated"

    def check_text_in_selector(self, project_name):
        with allure.step('Проверка наличия текста на странице'):
            self.actions.assert_text_in_element(self.message_created_project_locator,f'Project "{project_name}" has been successfully created. You can now create a build configuration.')

class OptionsProjectCreatedFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.actions_button = '.popupLink[type="button"] >> text=" Actions "'
        self.go_to_project_page_button = 'a.buildTypeName >> text="Go to project page"'
        self.delete_project_button = 'a[title="Delete project"]'
        self.copy_project_button = 'a[title="Copy project"]'
        self.copy_button = '#copyButton'
        self.after_copy_message = '#message_projectCopied'
        self.after_delete_message = '#message_projectRemoved'
        self.project_id_selector = "input#externalId"
        self.new_project_id = '#newProjectExternalId'
        self.message_error_empty_id = '#error_newProjectExternalId'

    def delete_project(self):
        with allure.step("Клик на кнопку actions на странице проекта"):
            self.actions.wait_for_selector(self.actions_button)
            self.actions.is_button_active(self.actions_button)
            self.actions.click_button(self.actions_button)
            time.sleep(2)
        with allure.step("Клик на кнопку удаления на странице проекта"):
            self.actions.wait_for_selector(self.delete_project_button)
            self.actions.assert_text_in_element(self.delete_project_button, "Delete project...")
            self.actions.is_button_active(self.delete_project_button)
            self.actions.click_button(self.delete_project_button)
            self.actions.wait_for_selector(self.after_delete_message)
            # todo self.actions.assert_text_in_element(self.after_delete_message, f'Project "{name}" has been moved to the "config/_trash" directory. All project related data (build history, artifacts, and so on) will be cleaned from the database during the next clean-up. See clean-up policy configuration.You can undo the deletion by moving the "config/_trash/{project_id}.project17024" to the "config/projects/{project_id}" manually')

    def copy_project(self, project_id):
        with allure.step("Клик на кнопку actions на странице проекта"):
            self.actions.wait_for_selector(self.actions_button)
            self.actions.is_button_active(self.actions_button)
            self.actions.click_button(self.actions_button)
            time.sleep(2)
            self.actions.wait_for_selector(self.copy_project_button)
            time.sleep(2)
        with allure.step("Клик на кнопку copy для копирования проекта"):
            self.actions.is_element_present(self.copy_project_button)
            self.actions.click_button(self.copy_project_button)
            self.actions.wait_for_selector(self.copy_button)
            time.sleep(2)
        with allure.step("Добавления нового проджект id в поле project id"):
            self.actions.input_text(self.new_project_id, project_id)
            time.sleep(2)
        with allure.step("Клик на кнопку копирования проекта"):
            self.actions.is_element_present(self.copy_button)
            self.actions.click_button(self.copy_button)
            self.actions.wait_for_selector(self.after_copy_message)
        with allure.step("Проверка отображения текста об успешном копировании проекта"):
            self.actions.assert_text_in_element(self.after_copy_message,'Project has been copied successfully. Project name has been changed because another project with the same name already exists. Project-associated settings were copied.')

    def copy_project_with_empty_id(self, project_id):
        with allure.step("Клик на кнопку actions на странице проекта"):
            self.actions.wait_for_selector(self.actions_button)
            self.actions.is_button_active(self.actions_button)
            self.actions.click_button(self.actions_button)
            time.sleep(2)
            self.actions.wait_for_selector(self.copy_project_button)
        with allure.step("Клик на кнопку copy для копирования проекта"):
            self.actions.click_button(self.copy_project_button)
            time.sleep(2)
            self.actions.wait_for_selector(self.copy_button)
        with allure.step("Добавления нового проджект id в поле project id"):
            self.actions.input_text(self.new_project_id, project_id)
            time.sleep(2)
            self.actions.is_element_present(self.copy_button)
        with allure.step("Клик на кнопку копирования проекта"):
            self.actions.click_button(self.copy_button)
            time.sleep(2)
            self.actions.wait_for_selector(self.message_error_empty_id)
        with allure.step("Проверка отображения текста об ошибке копирования проекта (project id пустой)"):
            self.actions.assert_text_in_element(self.message_error_empty_id,'Project ID must not be empty.')

class EditProjectPageFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_selector = "input#name"
        self.project_id_selector = "input#externalId"
        self.project_description_selector = "input#description"
        self.project_save_button_selector = '.submitButton[name="submitButton"]'
        self.project_cancel_button_selector = ".cancel"


    def input_project_edit_details(self, name, project_id, description):
        with allure.step("Ввод данных для изменения проекта"):
            self.actions.wait_for_selector(self.project_name_selector)
            self.actions.input_text(self.project_name_selector, name)
            time.sleep(2)
            self.actions.input_text(self.project_id_selector, project_id)
            time.sleep(2)
            self.actions.input_text(self.project_description_selector, description)

    def check_project_details(self, name, project_id, description):
        with allure.step("Проверка данных проекта"):
            self.actions.assert_element_attribute(self.project_name_selector, "value", f"{name}")
            self.actions.assert_element_attribute(self.project_id_selector, "value", f"{project_id}")
            self.actions.assert_element_attribute(self.project_description_selector, "value", f"{description}")

    def check_project_name(self, name):
        with allure.step("Проверка имени проекта"):
            self.actions.assert_element_attribute(self.project_name_selector, "value", f"{name}")

    def click_save_project_edit_button(self):
        with allure.step("Нажатие кнопки изменения созданного проекта"):
            self.actions.is_element_present(self.project_save_button_selector)
            self.actions.click_button(self.project_save_button_selector)

    def click_cancel_project_edit_button(self):
        with allure.step("Нажатие кнопки отмены изменения созданного проекта"):
            self.actions.is_element_present(self.project_cancel_button_selector)
            self.actions.click_button(self.project_cancel_button_selector)


class AddBuildConf(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.build_conf_add_button_selector = 'span.addNew:has-text("Create build configuration")'
        self.build_conf_templates_button_selector = 'span.addNew:has-text("Create template")'
        self.subproject_button_selector = 'span.addNew:has-text("Create subproject")'


    def click_on_create_build_cond(self):
        with allure.step("Нажатие кнопки создания билд конфигурации"):
            self.actions.wait_for_selector(self.build_conf_add_button_selector)
            self.actions.is_element_present(self.build_conf_add_button_selector)
            self.actions.click_button(self.build_conf_add_button_selector)


class EditProjectFormPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.message_created_project = MessageProjectCreatedFragment(page)
        self.edit_project_page = EditProjectPageFragment(page)
        self.add_build_conf = AddBuildConf(page)


    def go_to_edit_project_page(self):
        with allure.step("Переход на страницу редактирования проекта"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def check_project_data(self, name, project_id, description):
        self.message_created_project.check_text_in_selector(name)
        self.edit_project_page.check_project_details(name, project_id, description)
        time.sleep(2)
        with allure.step("Клик на кнопку создания проекта"):
            self.add_build_conf.click_on_create_build_cond()
            self.page_url = f"/admin/createObjectMenu.html?projectId={project_id}&showMode=createBuildTypeMenu&cameFromUrl=%2Fadmin%2FeditProject.html%3FprojectId%3D{project_id}"
            self.actions.wait_for_url_change(self.page_url)


class EditProjectFormWithWrongIdPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.message_created_project = MessageProjectCreatedFragment(page)
        self.edit_project_page = EditProjectPageFragment(page)
        self.add_build_conf = AddBuildConf(page)
        self.invalid_id_error = '#errorExternalId'
        self.warning_message ='#changeExternalIdWarning'


    def go_to_edit_project_page(self):
            with allure.step("Переход на страницу редактирования проекта"):
                self.actions.navigate(self.page_url)
                self.actions.wait_for_page_load(self.page_url)

    def edit_project_data_with_invalid_id(self, name, project_id, description):
        with allure.step("Переход на страницу редактирования проекта"):
            self.message_created_project.check_text_in_selector(name)
            time.sleep(2)
        with allure.step("Добавление информации в поля для редактирования проекта"):
            self.edit_project_page.input_project_edit_details(name, project_id, description)
            time.sleep(2)
            self.actions.wait_for_selector(self.warning_message)
        with allure.step("Проверка отображения сообщения об предупреждении project id"):
            self.actions.assert_text_in_element(self.warning_message, 'Important: Modifying the ID will change all the URLs related to the project. It is highly recommended to update the ID in any of the URLs bookmarked or hard-coded in the scripts. The corresponding configuration and artifacts directory names on the disk will change too and it can take time.')
        with allure.step("Клик на кнопку сохранения данных редактирования проекта"):
            self.edit_project_page.click_save_project_edit_button()
            time.sleep(2)
        with allure.step("Проверка отображения сообщения об ошибке при редактировании проекта (невалидный project id)"):
            self.actions.wait_for_selector(self.invalid_id_error)
            self.actions.assert_text_in_element(self.invalid_id_error, f"Project ID \"{project_id}\" is invalid: starts with non-letter character '{project_id[0]}'. ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters).")


class EditProjectFormWithChangesPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.message_created_project = MessageProjectCreatedFragment(page)
        self.edit_project_page = EditProjectPageFragment(page)
        self.add_build_conf = AddBuildConf(page)
        self.message_success = '#message_projectUpdated'


    def go_to_edit_project_page(self):
        with allure.step("Переход на страницу редактирования проекта"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def change_project_data(self, name, project_id, description):
        with allure.step("Добавление информации в поля для редактирования проекта"):
            self.edit_project_page.input_project_edit_details(name, project_id, description)
            time.sleep(2)
        with allure.step("Клик на кнопку сохранения данных редактирования проекта"):
            self.edit_project_page.click_save_project_edit_button()
        with allure.step("Отображения сообщения об успешном сохранении данных редактирования проекта"):
            self.actions.wait_for_selector(self.message_success)
            self.actions.assert_text_in_element(self.message_success, 'Your changes have been saved.')
            self.page_url = f'/admin/editProject.html?projectId={project_id}'
            self.actions.wait_for_url_change(self.page_url)

class DeleteProjectPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.options_project = OptionsProjectCreatedFragment(page)


    def delete_project(self):
        self.options_project.delete_project()


class CopyProjectPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/editProject.html?projectId={project_id}')
        self.options_project = OptionsProjectCreatedFragment(page)
        self.project_data_fields = EditProjectPageFragment(page)


    def copy_project(self, project_id):
        with allure.step("Копирование проекта"):
            self.options_project.copy_project(project_id)

    def copy_project_with_empty_id(self, project_id):
        with allure.step("Копирование проекта с пустым project id"):
            self.options_project.copy_project_with_empty_id(project_id)





