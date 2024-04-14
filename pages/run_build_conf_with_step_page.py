import allure
from pages.base_page import BasePage


class StepAddMessageFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.step_add_message_selector = ("div#unprocessed_build"
                                          "RunnerSettingsUpdated")

    def check_text_in_selector(self):
        with allure.step("Проверка наличия текста на странице"):
            self.actions.wait_for_selector(self.step_add_message_selector)
            self.actions.assert_text_in_element(
                self.step_add_message_selector, "Build step settings updated."
            )


class WrapperRunBuildConfWithStep(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.run_build_conf_with_step_selector = ("#breadcrumbsWrapper"
                                                  " > div.quickLinks"
                                                  " > div:nth-child(1)"
                                                  " > span > button"
                                                  ":nth-child(1)")

    def click_run_build_conf(self):
        with allure.step("Запуск билд кофигурации с шагом"):
            self.actions.click_button(
                self.run_build_conf_with_step_selector
            )

    def is_run_build_active(self):
        with allure.step("Активность кнопки запуска билд конфигурации"):
            return self.actions.is_element_visible(
                self.run_build_conf_with_step_selector
            )


class RunBuildWithStep(BasePage):
    def __init__(self, page, build_conf_id):
        super().__init__(page)
        self.page_url = (f"/admin/editBuildRunners.html?id=buildType"
                         f":{build_conf_id}")
        self.success_message = StepAddMessageFragment(page)
        self.run_build_with_step = WrapperRunBuildConfWithStep(page)

    def go_to_build_steps_page(self):
        with allure.step(
            "Переход на стр с отображением шагов к билд конф"
        ):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def check_url_change(self, build_conf_id):
        with allure.step(
            "Проверка изменения url страницы"
        ):
            self.page_url = (f"/admin/editBuildRunners.html?id=buildType"
                             f":{build_conf_id}")
            self.actions.wait_for_url_change(self.page_url)

    def run_build_conf_with_step(self):
        with allure.step(
            "Текст об успешном добавлении шагов к билд конф"
        ):
            self.success_message.check_text_in_selector()
        with allure.step("Клик по кнопке запуска билда"):
            self.run_build_with_step.is_run_build_active()
            self.run_build_with_step.click_run_build_conf()
