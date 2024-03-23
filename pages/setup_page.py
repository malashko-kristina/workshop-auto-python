import time
import allure
from pages.base_page import BasePage

class FirstStartWindow(BasePage):

    def __init__(self, page):
        self.page = page
        super().__init__(page)
        self.page_url = '/mnt'
        self.first_title = "#pageContent > h1"
        self.restore_button = "input#restoreButton"
        self.proceed_button = "input#proceedButton"
        self.data_base_title = "#pageContent > h1"


    def is_restore_button_active(self):
        with allure.step("Проверка активности кнопки restore"):
            self.actions.is_button_active(self.restore_button)

    def click_on_restore_button(self):
        with allure.step("Клик по кнопке restore"):
            self.actions.click_button(self.restore_button)

    def is_proceed_button_active(self):
        with allure.step("Проверка активности кнопки proceed"):
            self.actions.wait_for_selector(self.proceed_button, timeout="30000")

    def click_on_proceed_button(self):
        with allure.step("Клик по кнопке proceed"):
            self.actions.click_button(self.proceed_button)


    def proceed_step(self):
        self.actions.wait_for_page_load()
        self.is_proceed_button_active()
        self.click_on_proceed_button()



class Loading(BasePage):
    def __init__(self, page):
        self.page = page
        super().__init__(page)


    def wait_loading(self):
        self.actions.wait_for_page_load()


class Agreement(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.page_url = "/showAgreement.html"
        self.check_box = "input#accept"
        self.continue_button = "input.btn.btn_primary.submitButton"

    def check_in_box(self):
        self.actions.wait_for_selector(self.check_box)
        self.actions.check_box(self.check_box)


    def continue_agreement(self):
        self.actions.is_button_active(self.continue_button)
        self.actions.click_button(self.continue_button)


class SetUpUser(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.page_url = "/showAgreement.html"
        self.username_field = "input#input_teamcityUsername"
        self.password_field = "input#password1"
        self.repeat_password_field = "input#retypedPassword"
        self.create_account_button = "input.btn.loginButton[value='Create Account']"


    def fill_user_data(self, username, password):
        self.actions.wait_for_page_load()
        self.actions.wait_for_selector(self.username_field)
        self.actions.input_text(self.username_field, username)
        time.sleep(2)
        self.actions.wait_for_selector(self.password_field)
        self.actions.input_text(self.password_field, password)
        time.sleep(2)
        self.actions.wait_for_selector(self.repeat_password_field)
        self.actions.input_text(self.repeat_password_field, password)
        time.sleep(2)


    def create_user(self):
        self.actions.is_button_active(self.create_account_button)
        self.actions.click_button(self.create_account_button)



class SetUpPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.page_url = '/mnt'
        self.first_start_window = FirstStartWindow(self.page)
        self.loading = Loading(self.page)
        self.agreement = Agreement(self.page)
        self.setup_user = SetUpUser(self.page)

    def set_up(self, username="admin", password="admin"):
        with allure.step("Переход на самую первую приветственную страницу"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()
        with allure.step("Клик на кнопку продолжить на странице 'First Start'"):
            time.sleep(2)
            self.first_start_window.proceed_step()
            time.sleep(2)
            self.loading.wait_loading()
        with allure.step("Клик на кнопку продолжить на странице 'DataBase connection setup'"):
            time.sleep(2)
            self.first_start_window.proceed_step()
            self.loading.wait_loading()
        with allure.step("Добавление флажка в чекбокс о принятии лицензионного соглашения"):
            time.sleep(3)
            self.agreement.check_in_box()
        with allure.step("Проверка перехода на страницу 'License Agreement'"):
            self.actions.check_url(self.agreement.page_url)
        with allure.step("Клик на кнопку продолжить после принятия лицензионного соглашения"):
            time.sleep(2)
            self.agreement.continue_agreement()
            self.actions.wait_for_page_load()
        with allure.step("Заполнение данных пользователя для его создания"):
            self.setup_user.fill_user_data(username, password)
        with allure.step("Клик на кнопку создания пользователя"):
            self.setup_user.create_user()
        with allure.step("Проверка перехода на страницу логина"):
            self.page_url = "/favorite/projects"
            self.actions.wait_for_url_change(self.page_url)
