import allure
from pages.base_page import BasePage


class SideBarListBuildConfFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.create_build_from_url = "a.tabs:has-text('Build Steps')"

    def click_create_steps_build_conf(self):
        with allure.step("Select creation steps for build config"):
            self.actions.click_button(self.create_build_from_url)

    def is_build_steps_active(self):
        with allure.step(
            "Activity of the button for creating steps for build config"
        ):
            return self.actions.is_element_visible(
                self.create_build_from_url
            )


class BreadCrumbsWrapperRunBuildConf(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.run_build_conf_selector = "button.btn_mini"

    def click_run_build_conf(self):
        with allure.step("Launch build configuration"):
            self.actions.click_button(self.run_build_conf_selector)

    def is_run_build_active(self):
        with allure.step("Activity of the build configuration launch button"):
            return self.actions.is_element_visible(
                self.run_build_conf_selector
            )


class BuildConfRunPage(BasePage):
    def __init__(self, page, project_id, build_conf_id):
        super().__init__(page)
        self.page_url = (f"/admin/editBuildTypeVcsRoots.html?init="
                         f"1&id=buildType:{build_conf_id}&cameFromUrl"
                         f"=%2Fadmin%2FeditProject.html%3Finit%3D1%2"
                         f"6projectId%3D{project_id}")
        self.run_build_conf_wrapper = BreadCrumbsWrapperRunBuildConf(page)
        self.create_steps_build_conf_bar = SideBarListBuildConfFragment(page)

    def go_to_creation_build_conf_page(self):
        with allure.step("Go to the build configuration launch page"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def tap_on_add_build_steps(self):
        with allure.step(
            "Go to the page for creating steps for the build configuration"
        ):
            self.create_steps_build_conf_bar.is_build_steps_active()
            self.create_steps_build_conf_bar.click_create_steps_build_conf()

    def run_build_conf_ui(self):
        with allure.step("Run build configuration without adding steps"):
            self.run_build_conf_wrapper.click_run_build_conf()
            self.actions.wait_for_url_change(self.page_url)
