import allure
from pages.base_page import BasePage

class MenuListCreateFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.create_from_url_selector = ("a.createOption:has-text"
                                         "('From a repository URL')")
        self.create_manually_selector = ("a.createOption:"
                                         "has-text(' Manually')")

    def click_create_from_url(self):
        with allure.step('Выбор создания проекта по url'):
            self.actions.click_button(self.create_from_url_selector)

    def click_create_manually(self):
        with allure.step('Выбор создания проекта вручную'):
            self.actions.is_element_visible(self.create_manually_selector)
            self.actions.click_button(self.create_manually_selector)

    def is_create_from_url_active(self):
        with allure.step('Проверка активности кнопки создания проекта по url'):
            return self.actions.is_element_visible(self.create_from_url_selector)

    def is_create_manually_active(self):
        with allure.step('Проверка активности кнопки создания проекта вручную'):
            return self.actions.is_element_visible(self.create_manually_selector)


class CreateFormContainerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_selector = "input#name"
        self.project_id_selector = "input#externalId"
        self.project_description_selector = "input#description"
        self.create_project_button = 'input#createProject'
        self.error_empty_name = "#errorName"
        self.error_used_id = "#errorExternalId"

    def input_project_details(self, name, project_id, description):
        with allure.step("Ввод данных для создания проекта"):
            self.actions.wait_for_selector(self.project_name_selector)
            self.actions.input_text(self.project_name_selector, name)
            self.actions.input_text(self.project_id_selector, project_id)
            self.actions.input_text(self.project_description_selector, description)

    def click_create_button(self):
        with allure.step("Нажатие кнопки создания проекта"):
            self.actions.wait_for_page_load()
            self.actions.wait_for_selector(self.create_project_button)
            self.actions.is_button_active(self.create_project_button)
            self.actions.click_button(self.create_project_button)

    def error_empty_project_name(self):
        with allure.step(f"Проверка нахождения текста об ошибке"
                         f" 'Project name is empty' в селекторе"
                         f" {self.error_empty_name}"):
            self.actions.wait_for_selector(self.error_empty_name)
            self.actions.assert_text_in_element(self.error_empty_name,
                                                "Project name is empty")
            self.actions.check_error_text_color(self.error_empty_name)
    def error_invalid_project_id(self, project_id):
        with allure.step(f"Проверка нахождения текста об ошибке"
                         f" \"f\'Project ID \"{project_id}\" is already"
                         f" used by another project\'\" в селекторе"
                         f" {self.error_used_id}"):
            self.actions.assert_text_in_element(self.error_used_id,
                                                f'Project ID "{project_id}"'
                                                f' is already used by another project')
            self.actions.check_error_text_color(self.error_used_id)


class ProjectCreationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/admin/createObjectMenu.html?projectId='
                         '_Root&showMode=createProjectMenu'
                         '&cameFromUrl=http%3A%2F%2Flocalhost%3A81'
                         '11%2Ffavorite%2Fprojects')
        self.menu_list_create = MenuListCreateFragment(page)
        self.create_form_container = CreateFormContainerFragment(page)

    def check_project_creation_page_url(self, url=None):
        if url is None:
            url = self.page_url
        self.actions.check_url(url, equal=False)

    def go_to_creation_page(self):
        with allure.step("Переход на страницу создания проекта"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_project_manually(self, name, project_id, description):
        with allure.step("Клик по кнопке ручного создания проекта"):
            self.menu_list_create.click_create_manually()
        with allure.step("Заполнение полей информации о проекте"):
            self.create_form_container.input_project_details(
                name, project_id, description)
        with allure.step("Клик по кнопке создания проекта"):
            self.create_form_container.click_create_button()
            self.actions.wait_for_page_load()

    def check_url_after_project_creation(self, project_id):
        with allure.step("Проверка загрузки страницы после создания проекта"):
            self.page_url = (f'/admin/editProject.html?projectId={project_id}')
            self.actions.wait_for_page_load()
            self.actions.check_url(self.page_url)

    def check_error_empty_project_name_is_visible(self):
        with allure.step(f"Проверка нахождения текста об ошибке"
                         f" 'Project name is empty' в селекторе"
                         f" {self.create_form_container.error_empty_name}"):
            self.create_form_container.error_empty_project_name()

    def check_error_invalid_project_id_is_visible(self, project_id):
        with allure.step(f"Проверка нахождения текста об ошибке"
                         f" о том, что project id уже используется"):
            self.create_form_container.error_invalid_project_id(project_id)



