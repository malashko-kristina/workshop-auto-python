import allure
from pages.base_page import BasePage

class LoginFormBody(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_locator = "#username"
        self.password_locator = "#password"
        self.login_button_locator = "input.loginButton[name='submitLogin']"
        self.userpic = 'span[data-test="avatar"]'

    def input_user_details(self, login, password):
        with allure.step("Ввод данных для юзера"):
            self.actions.wait_for_selector(self.username_locator)
            self.actions.input_filtred_text(self.username_locator, login)
            self.actions.input_filtred_text(self.password_locator, password)

    def click_login_button(self):
        with allure.step("Клик на кнопку логина для входа в систему"):
            self.actions.is_button_active(self.login_button_locator)
            self.actions.wait_for_selector(self.login_button_locator)
            self.actions.click_button(self.login_button_locator)

    def userpic_is_visible(self):
        with allure.step('Проверка видимости юзерпика'):
            self.actions.wait_for_selector(self.userpic)
            self.actions.is_element_visible(self.userpic)


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = '/login.html'
        self.login_form_body = LoginFormBody(page)

    def go_to_login_page(self):
        with allure.step("Переход на страницу логина"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def check_url_favourite_projects_mode(self):
        with allure.step("Проверка страницы по url /favorite/projects?mode=builds"):
            self.page_url = "/favorite/projects?mode=builds"
            self.actions.check_url(self.page_url, equal=False)

    def check_url_favourite_projects(self):
        self.page_url = "/favorite/projects"
        with allure.step("Проверка перехода по url /favorite/projects (для самого первого проекта)"):
            self.actions.check_url(self.page_url, equal=False)

    def login_in_account(self, login, password):
        self.go_to_login_page()
        with allure.step("Ввод логина и пароля юзера"):
            self.login_form_body.input_user_details(login, password)
        with allure.step("Клик на кнопку логина в аккаунт"):
            self.login_form_body.click_login_button()

