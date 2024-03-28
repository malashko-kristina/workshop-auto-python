import allure
from pages.agents_page import AgentsPage
from pages.login_page import LoginFormBody
from pages.setup_page import SetUpPage

@allure.title("Настройка сервера")
@allure.description("Настраиваем проект, принимая пользовательские соглашения, инициализируя БД, создавая админ юзера")
def test_set_up(one_browser):
    with allure.step("Setup Тимсити сервера"):
        set_up_page = SetUpPage(one_browser)
        set_up_page.set_up()
    with allure.step("Проверка перехода на Home page"):
        after_login = LoginFormBody(one_browser)
        after_login.userpic_is_visible()
    with allure.step("Авторизация нового неавторизованного тимсити агента"):
        agents_page = AgentsPage(one_browser)
        agents_page.authorize_agent()