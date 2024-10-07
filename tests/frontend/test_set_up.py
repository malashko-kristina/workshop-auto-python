import allure
import pytest
from pages.agents_page import AgentsPage
from pages.login_page import LoginFormBody
from pages.setup_page import SetUpPage


@allure.title("Set up the server")
@allure.description("We set up the project by accepting user agreements, initializing the database,"
                    " creating an admin user")
@pytest.mark.swagger_coverage_exl
def test_set_up(one_browser):
    with allure.step("Setup Timcity server"):
        set_up_page = SetUpPage(one_browser)
        set_up_page.set_up()
    with allure.step("Check the transition to the Home page"):
        after_login = LoginFormBody(one_browser)
        after_login.userpic_is_visible()
    with allure.step("Authorization of a new unauthorized teamcity agent"):
        agents_page = AgentsPage(one_browser)
        agents_page.authorize_agent()
