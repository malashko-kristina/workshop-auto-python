import allure
from pages.base_page import BasePage


class FormNewBuildStepsFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.step_name_selector = "input#buildStepName"
        self.step_id_selector = "input#newRunnerId"
        self.step_custom_script_selector = ".CodeMirror >> textarea"
        self.step_submit_button_selector = (
            "input.btn.btn_primary.submitButton" "[name='submitButton']"
        )
        self.step_cancel_button_script_selector = "a.cancel"
        self.error_empty_custom_script = ".error.expanded_true"
        self.error_step_id = "#error_newRunnerId"

    def input_step_details(self, step_name, step_id, text):
        with allure.step("Input data for creating a step for the build configuration"):
            self.actions.wait_for_selector(self.step_name_selector)
            self.actions.input_text(self.step_name_selector, step_name)
            self.actions.input_text(self.step_id_selector, step_id)
            self.actions.input_text(self.step_custom_script_selector, text)

    def click_add_new_step(self):
        with allure.step("Clicking the button to add a step to the build configuration"):
            self.actions.click_button(self.step_submit_button_selector)

    def is_add_new_active(self):
        with allure.step("Checking the activity of the add step button"):
            self.actions.is_button_active(self.step_submit_button_selector)

    def check_error_message_empty_script(self):
        with allure.step("Checking for an empty field command line error"):
            self.actions.wait_for_selector(self.error_empty_custom_script)
            self.actions.assert_text_in_element(
                self.error_empty_custom_script,
                "Script content must be specified"
            )
            self.actions.check_error_color(self.error_step_id)

    def check_error_message_empty_step_id(self):
        with allure.step("Checking for an empty field ID step error"):
            self.actions.wait_for_selector(self.error_step_id)
            self.actions.assert_text_in_element(
                self.error_step_id,
                "Build step ID must not be empty."
            )
            self.actions.check_error_color(self.error_step_id)

    def error_message_invalid_step_id(self, build_step_id, first_symbol):
        with allure.step("Checking for an invalid field ID step error"):
            self.actions.wait_for_selector(self.error_step_id)
            self.actions.assert_text_in_element(
                self.error_step_id,
                f'Build step ID "{build_step_id}" is invalid:'
                f" starts with non-letter character '{first_symbol}'."
                f" ID should start with a latin letter and contain only"
                f" latin letters, digits and underscores"
                f" (at most 80 characters).",
            )
            self.actions.check_error_color(self.error_step_id)


class ContentNewBuildStepCommandLineFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.add_command_line_button_selector = (
            "td.SelectBuildRunners__title--" "Vf:has-text('Command Line')"
        )

    def click_command_line(self):
        with allure.step("Clicking the button to add a command line"):
            self.actions.click_button(self.add_command_line_button_selector)

    def is_build_steps_active(self):
        with allure.step("Checking the activity of the add command line button"):
            return self.actions.is_element_visible(
                self.add_command_line_button_selector
            )


class BuildNewStepPage(BasePage):
    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (
            f"/admin/editRunType.html?id=buildType:{build_conf_id}"
            f"&runnerId=__NEW_RUNNER__&cameFromUrl=%2Fadmin%2FeditBuild"
            f"Runners.html%3Fid%3DbuildType%253A{build_conf_id}"
            f"%26init%3D1&cameFromTitle="
        )
        self.command_line_add = ContentNewBuildStepCommandLineFragment(page)
        self.add_build_steps = FormNewBuildStepsFragment(page)

    def go_to_build_steps_page(self):
        with allure.step("Navigating to the add steps page for the build configuration"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def select_command_line(self):
        with allure.step("Selecting command line as a step for the build configuration"):
            self.command_line_add.is_build_steps_active()
            self.command_line_add.click_command_line()

    def add_new_build_step(self, step_name, step_id, text):
        with allure.step("Filling in the fields to add a command line"):
            self.add_build_steps.input_step_details(step_name, step_id, text)
        with allure.step("Clicking the button to add a step to the build configuration"):
            self.add_build_steps.is_add_new_active()
            self.add_build_steps.click_add_new_step()

    def check_url_after_step_add(self, build_conf_id):
        self.page_url = (
            f"/admin/editRunType.html?id=buildType:"
            f"{build_conf_id}&runnerId=__NEW_RUNNER__&came"
            f"FromUrl=%2Fadmin%2FeditBuildRunners.html%3Fid"
            f"%3DbuildType%253A{build_conf_id}%26init%3D1&"
            f"cameFromTitle="
        )
        self.actions.wait_for_url_change(self.page_url)

    def check_error_message_empty_step_id(self):
        with allure.step("Checking for an error about an empty step ID"):
            self.add_build_steps.check_error_message_empty_step_id()

    def check_error_message_invalid_step_id(self, build_step_id, first_symbol):
        with allure.step("Checking for an error about an invalid step ID"):
            self.add_build_steps.error_message_invalid_step_id(
                build_step_id, first_symbol
            )

    def check_error_message_empty_custom_script(self):
        with allure.step("Checking for an error regarding an empty command line field"):
            self.add_build_steps.check_error_message_empty_script()

    def wait_for_current_page_load(self):
        with allure.step("Checking the page loading"):
            self.actions.wait_for_page_load()
