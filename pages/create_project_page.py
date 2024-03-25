import time
import allure
from pages.base_page import BasePage

class MenuListCreateFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.create_from_url_selector = "a.createOption:has-text('From a repository URL')"
        self.create_manually_selector = "a.createOption:has-text(' Manually')"


    def click_create_from_url(self):
        with allure.step('Выбор создания проекта по url'):
            self.actions.click_button(self.create_from_url_selector)

    def click_create_manually(self):
        with allure.step('Выбор создания проекта вручную'):
            self.actions.click_button(self.create_manually_selector)

    def is_create_from_url_active(self):
        with allure.step('Проверка активности кнопки создания проекта по url'):
            return self.actions.is_element_present(self.create_from_url_selector)

    def is_create_manually_active(self):
        with allure.step('Проверка активности кнопки создания проекта вручную'):
            return self.actions.is_element_present(self.create_manually_selector)


class CreateFormContainerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_selector = "input#name"
        self.project_id_selector = "input#externalId"
        self.project_description_selector = "input#description"
        self.create_project_button = 'input.btn.btn_primary.submitButton[id="createProject"]'

    def input_project_details(self, name, project_id, description):
        with allure.step("Ввод данных для создания проекта"):
            self.actions.wait_for_selector(self.project_name_selector)
            self.actions.input_text(self.project_name_selector, name)
            time.sleep(2)
            self.actions.input_text(self.project_id_selector, project_id)
            time.sleep(2)
            self.actions.input_text(self.project_description_selector, description)
            time.sleep(2)

    def click_create_button(self):
        with allure.step("Нажатие кнопки создания проекта"):
            self.actions.is_element_present(self.create_project_button)
            self.actions.click_button(self.create_project_button)


class ProjectCreationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects%3Fmode%3Dbuilds')
        self.menu_list_create = MenuListCreateFragment(page)
        self.create_form_container = CreateFormContainerFragment(page)

    def go_to_creation_page(self):
        with allure.step("Переход на страницу создания проекта"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_project(self, name, project_id, description):
        with allure.step("Переход на страницу создания проекта"):
            self.go_to_creation_page()
            time.sleep(2)
        with allure.step("Клик по кнопке ручного создания проекта"):
            self.menu_list_create.click_create_manually()
            time.sleep(2)
        with allure.step("Заполнение полей информации о проекте"):
            self.create_form_container.input_project_details(name, project_id, description)
            time.sleep(2)
        with allure.step("Клик по кнопке создания проекта"):
            self.create_form_container.click_create_button()
            time.sleep(3)
        with allure.step("Проверка загрузки страницы"):
            self.page_url = (f'/admin/editProject.html?projectId={project_id}')
            self.actions.wait_for_page_load()
            self.actions.check_url(self.page_url, timeout=90000)



class ProjectCreationPageThroughHeader(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects#createManually')
        self.menu_list_create = MenuListCreateFragment(page)
        self.create_form_container = CreateFormContainerFragment(page)

    def create_project(self, name, project_id, description):
        with allure.step("Клик по кнопке ручного создания проекта"):
            self.menu_list_create.is_create_from_url_active()
            self.menu_list_create.click_create_manually()
            time.sleep(2)
        with allure.step("Проверка текущей ссылки создания проекта"):
            self.actions.check_url(self.page_url, timeout=90000)
        with allure.step("Заполнение полей информации о проекте"):
            self.create_form_container.input_project_details(name, project_id, description)
            time.sleep(2)
        with allure.step("Клик по кнопке создания проекта"):
            self.create_form_container.click_create_button()
            time.sleep(2)
        with allure.step("Проверка загрузки страницы"):
            self.page_url = (f'/admin/editProject.html?projectId={project_id}')
            time.sleep(3)
            self.actions.wait_for_page_load()
            self.actions.check_url(self.page_url, timeout=90000)



class ProjectCreationPageWithEmptyName(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects%3Fmode%3Dbuilds')
        self.menu_list_create = MenuListCreateFragment(page)
        self.create_form_container = CreateFormContainerFragment(page)
        self.error_empty_name = "#errorName"

    def go_to_creation_page(self):
        with allure.step("Переход на страницу создания проекта"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_project(self, name, project_id, description):
        with allure.step("Переход на страницу создания проекта"):
            self.go_to_creation_page()
            time.sleep(2)
        with allure.step("Клик по кнопке ручного создания проекта"):
            self.menu_list_create.click_create_manually()
            time.sleep(2)
        with allure.step("Заполнение полей информации о проекте"):
            self.create_form_container.input_project_details(name, project_id, description)
            time.sleep(2)
        with allure.step("Клик по кнопке создания проекта"):
            self.create_form_container.click_create_button()
            time.sleep(2)
            self.actions.wait_for_selector(self.error_empty_name)
            time.sleep(2)
        with allure.step(f"Проверка нахождения текста об ошибке 'Project name is empty' в селекторе {self.error_empty_name}"):
            self.actions.assert_text_in_element(self.error_empty_name, "Project name is empty")
            self.actions.check_error_text_color(self.error_empty_name)

class ProjectCreationPageWithUsedId(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects%3Fmode%3Dbuilds')
        self.menu_list_create = MenuListCreateFragment(page)
        self.create_form_container = CreateFormContainerFragment(page)
        self.error_used_id = "#errorExternalId"

    def go_to_creation_page(self):
        with allure.step("Переход на страницу создания проекта"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_project(self, name, project_id, description):
        with allure.step("Клик по кнопке ручного создания проекта"):
            self.menu_list_create.is_create_manually_active()
            self.menu_list_create.click_create_manually()
            time.sleep(2)
        with allure.step("Заполнение полей информации о проекте"):
            self.create_form_container.input_project_details(name, project_id, description)
            time.sleep(2)
        with allure.step("Клик по кнопке создания проекта"):
            self.create_form_container.click_create_button()
            time.sleep(2)
            self.actions.wait_for_selector(self.error_used_id)
            time.sleep(2)
        with allure.step(f"Проверка нахождения текста об ошибке \"f\'Project ID \"{project_id}\" is already used by another project\'\" в селекторе {self.error_used_id}"):
            self.actions.assert_text_in_element(self.error_used_id, f'Project ID "{project_id}" is already used by another project')
            self.actions.check_error_text_color(self.error_used_id)


class CreateTheFirstProjectFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.welcome_text = 'div.UIPlaceholder__infoContainer--xa > h1.ring-heading-heading.ring-global-font'
        self.create_button_selector = 'a[data-test="create-project"]'


    def click_create_project_button(self):
        with allure.step('Клик по кнопке создания проекта'):
            self.actions.is_element_present(self.create_button_selector)
            self.actions.click_button(self.create_button_selector)


    def check_text_is_visible(self):
        with allure.step('Проверка видимости текста'):
            self.actions.wait_for_selector(self.welcome_text)
            self.actions.is_element_present(self.welcome_text)
            self.actions.assert_text_in_element(self.welcome_text, "Welcome to TeamCity")



class FirstCreateFormContainerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_selector = "input#name"
        self.project_id_selector = "input#externalId"
        self.project_description_selector = "input#description"
        self.create_project_button = 'input.btn.btn_primary.submitButton[id="createProject"]'


    def input_first_project_details(self, name, project_id, description):
        with allure.step("Ввод данных для создания проекта"):
            self.actions.wait_for_selector(self.project_name_selector)
            self.actions.input_text(self.project_name_selector, name)
            time.sleep(2)
            self.actions.input_text(self.project_id_selector, project_id)
            time.sleep(2)
            self.actions.input_text(self.project_description_selector, description)
            time.sleep(2)

    def click_create_first_project_button(self):
        with allure.step("Нажатие кнопки создания проекта"):
            self.actions.is_element_present(self.create_project_button)
            self.actions.click_button(self.create_project_button)


class CreateTheFirstProjectPage(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.create_the_first_project = CreateTheFirstProjectFragment(page)
        self.first_create_form = FirstCreateFormContainerFragment(page)
        self.menu_list = MenuListCreateFragment(page)
        self.page_url = "/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects#createManually"


    def create_first_project(self, name, project_id, description):
        with allure.step('Проверка приветственного текста'):
            self.create_the_first_project.check_text_is_visible()
            time.sleep(2)
        with allure.step('Клик по кнопке создания проекта для перехода на страницу создания проекта'):
            self.create_the_first_project.click_create_project_button()
            time.sleep(2)
        with allure.step("Клик на ручное создание проекта"):
            self.menu_list.click_create_manually()
        with allure.step("Проверка текущей ссылки создания проекта"):
            self.actions.wait_for_url_change(self.page_url)
        with allure.step("Ввод данных для создания проекта"):
            self.first_create_form.input_first_project_details(name, project_id, description)
            time.sleep(2)
        with allure.step('Клик по кнопке создания проекта'):
            self.first_create_form.click_create_first_project_button()
            self.page_url = (f'/admin/editProject.html?projectId={project_id}')
            time.sleep(3)
            self.actions.wait_for_page_load()
            self.actions.check_url(self.page_url, timeout=90000)


