import allure
from pages.base_page import BasePage

class ErrorMessageFragment(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.error_message_exit_code = "#.Description__text--yr >> text='Exit code 127 (Step: Command Line) (new)'"
        self.error_message_build_problem = '#buildProblemsPreview'

    def check_errors_on_screen(self):
        with allure.step('Проверка наличия текста ошибок на странице'):
            self.actions.is_element_present(self.error_message_exit_code)
            self.actions.check_error_text_color(self.error_message_exit_code)
            self.actions.is_element_present(self.error_message_build_problem)
            self.actions.assert_text_in_element(self.error_message_build_problem, "1 Build Problem, 1 new")
            self.actions.check_error_text_color(self.error_message_exit_code)


class CheckRunBuildErrors(BasePage):
    def __init__(self, page, run_id):
        super().__init__(page)
        # todo self.page_url = (f'/buildConfiguration/Testpr_Buildconf/{run_id}?expandBuildDeploymentsSection=false&hideTestsFromDependencies=false&hideProblemsFromDependencies=false&expandBuildProblemsSection=true')
        self.error_message = ErrorMessageFragment(page)


    # todo def go_to_build_run_failed_page(self):
        # todo  with allure.step("Переход на страницу с отображением шагов к билд конфигурации"):
        # todo self.actions.navigate(self.page_url)
    # todo self.actions.wait_for_page_load(timeout=10000)

    def run_build_conf_failed(self):
        with allure.step("Проверка ошибок на странице после неудачного запуска билда"):
            self.error_message.check_errors_on_screen()





