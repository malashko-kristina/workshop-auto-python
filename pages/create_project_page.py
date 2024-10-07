import allure
from pages.base_page import BasePage


class MenuListCreateFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.create_from_url_selector = "a.createOption:has-text" "('From a repository URL')"
        self.create_manually_selector = "a.createOption:has-text(' Manually')"

    def click_create_from_url(self):
        with allure.step("Selecting to create a project by url"):
            self.actions.click_button(
                self.create_from_url_selector
            )

    def click_create_manually(self):
        with allure.step("Select to create a project manually"):
            self.actions.is_element_visible(
                self.create_manually_selector
            )
            self.actions.click_button(self.create_manually_selector)

    def is_create_from_url_active(self):
        with (allure.step("Activity of the button for creating a project by url")):
            return self.actions.is_element_visible(
                self.create_from_url_selector
            )

    def is_create_manually_active(self):
        with allure.step("Activity of the button for creating a project manually"):
            return self.actions.is_element_visible(
                self.create_manually_selector
            )


class CreateFormContainerFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_selector = "input#name"
        self.project_id_selector = "input#externalId"
        self.project_description = "input#description"
        self.create_project_button = "input#createProject"
        self.error_empty_name = "#errorName"
        self.error_used_id = "#errorExternalId"

    def input_project_details(self, name, project_id, description):
        with allure.step("Enter data to create a project"):
            self.actions.wait_for_selector(self.project_name_selector)
            self.actions.input_text(self.project_name_selector, name)
            self.actions.input_text(self.project_id_selector,
                                    project_id)
            self.actions.input_text(self.project_description,
                                    description)

    def click_create_button(self):
        with allure.step("Click on Create Project button"):
            self.actions.wait_for_page_load()
            self.actions.wait_for_selector(self.create_project_button)
            self.actions.is_button_active(self.create_project_button)
            self.actions.click_button(self.create_project_button)

    def error_empty_project_name(self):
        with allure.step("Check for error text location 'Project name is empty'"):
            self.actions.wait_for_selector(self.error_empty_name)
            self.actions.assert_text_in_element(self.error_empty_name, "Project name is empty")
            self.actions.check_error_color(self.error_empty_name)

    def error_invalid_project_id(self, project_id):
        with allure.step(
            f"Check for error text location"
            f' "f\'Project ID "{project_id}" is already'
            f" used by another project'\" in the selector"
            f" {self.error_used_id}"
        ):
            self.actions.assert_text_in_element(
                self.error_used_id,
                f'Project ID "{project_id}"'
                f" is already used by another project",
            )
            self.actions.check_error_color(self.error_used_id)


class ProjectCreationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = (
            "/admin/createObjectMenu.html?projectId="
            "_Root&showMode=createProjectMenu"
            "&cameFromUrl=http%3A%2F%2Flocalhost%3A81"
            "11%2Ffavorite%2Fprojects"
        )
        self.menu_list_create = MenuListCreateFragment(page)
        self.create_form_container = CreateFormContainerFragment(page)

    def check_project_creation_page_url(self, url=None):
        if url is None:
            url = self.page_url
        self.actions.check_url(url, equal=False)

    def go_to_creation_page(self):
        with allure.step("Go to the project creation page"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_project_manually(self, name, project_id, description):
        with allure.step("Click on the button to manually create a project"):
            self.menu_list_create.click_create_manually()
        with allure.step("Fill in the project information fields"):
            self.create_form_container.input_project_details(name, project_id, description)
        with allure.step("Click on the button to create a project"):
            self.create_form_container.click_create_button()
            self.actions.wait_for_page_load()

    def check_url_after_prt_crt(self, project_id):
        with allure.step("Check page loading after project creation"):
            self.page_url = f"/admin/editProject.html?projectId={project_id}"
            self.actions.wait_for_page_load()
            self.actions.check_url(self.page_url)

    def check_error_empty_project_name_is_visible(self):
        with allure.step("Check for error text location 'Project name is empty'"):
            self.create_form_container.error_empty_project_name()

    def check_error_invalid_project_id_is_visible(self, project_id):
        with allure.step("Check for error text stating that project id is already in use"):
            self.create_form_container.error_invalid_project_id(project_id)
