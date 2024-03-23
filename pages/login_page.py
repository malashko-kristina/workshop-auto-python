import time
import allure
from pages.base_page import BasePage

class LoginFormBody(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_locator = "#username"
        self.password_locator = "#password"
        self.login_button_locator = "input.loginButton[name='submitLogin']"


    def input_user_details(self, login, password):
        with allure.step("Ввод данных для юзера"):
            self.actions.wait_for_selector(self.username_locator)
            time.sleep(2)
            self.actions.input_filtred_text(self.username_locator, login)
            time.sleep(2)
            self.actions.input_filtred_text(self.password_locator, password)
            time.sleep(2)

    def click_login_button(self):
        with allure.step("Клик на кнопку логина для входа в систему"):
            self.actions.is_button_active(self.login_button_locator)
            self.actions.click_button(self.login_button_locator)


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = '/login.html'
        self.login_form_body = LoginFormBody(page)

    def go_to_login_page(self):
        with allure.step("Переход на страницу логина"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def login_in_account(self, login, password):
        self.go_to_login_page()
        with allure.step("Ввод логина и пароля юзера"):
            self.login_form_body.input_user_details(login, password)
        with allure.step("Клик на кнопку логина в аккаунт"):
            self.login_form_body.click_login_button()
            time.sleep(2)
            self.page_url = "/favorite/projects?mode=builds"
            self.actions.wait_for_url_change(self.page_url)

class LoginPageFirstTime(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = '/login.html'
        self.login_form_body = LoginFormBody(page)

    def go_to_login_page(self):
        with allure.step("Переход на страницу логина"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def login_in_account(self, login, password):
        self.go_to_login_page()
        time.sleep(2)
        with allure.step("Ввод логина и пароля юзера"):
            self.login_form_body.input_user_details(login, password)
            time.sleep(2)
        with allure.step("Клик на кнопку логина в аккаунт"):
            self.login_form_body.click_login_button()
            time.sleep(2)
            self.page_url = "/favorite/projects"
        with allure.step("Проверка перехода на страницу предпочитаемых проектов"):
            self.actions.wait_for_url_change(self.page_url)



