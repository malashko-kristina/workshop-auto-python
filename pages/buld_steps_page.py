import allure
from pages.base_page import BasePage


class ContentBuildStepsFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.add_build_steps_btn = "a.btn:has-text('Add build step')"

    def click_create_steps_build_conf(self):
        with allure.step("Нажатия на кнопку добавления шагов к билд"):
            self.actions.click_button(self.add_build_steps_btn)

    def is_build_steps_active(self):
        with allure.step("Проверка активности кнопки создания шагов"):
            return self.actions.is_element_visible(self.add_build_steps_btn)


class BuildStepsPage(BasePage):
    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (
            f'/admin/editBuildRunners.html?id=buildType:"{build_conf_id}"'
        )
        self.content_build_steps = ContentBuildStepsFragment(page)

    def go_to_build_steps_page(self):
        with allure.step("Переход на страницу для добавления шагов"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def add_build_steps(self, build_conf_id):
        with allure.step("Клик по кнопке добавления шагов"):
            self.content_build_steps.is_build_steps_active()
            self.content_build_steps.click_create_steps_build_conf()
            self.page_url = (
                f"/admin/editRunType.html?id=buildType:"
                f"{build_conf_id}&runnerId=__NEW_RUNNER__"
                f"&cameFromUrl=%2Fadmin%2FeditBuildRunners."
                f"html%3Fid%3DbuildType%253A{build_conf_id}"
                f"%26init%3D1&cameFromTitle="
            )
            self.actions.wait_for_url_change(self.page_url)
