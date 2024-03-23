import allure
from pages.setup_page import SetUpPage

@allure.title("Настройка сервера")
@allure.description("Настраиваем проект, принимая пользовательские соглашения, инициализируя БД, создавая админ юзера")
def test_set_up(one_browser):
    with allure.step("Setup"):
        set_up_page = SetUpPage(one_browser)

        set_up_page.set_up()