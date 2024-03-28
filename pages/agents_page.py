import allure

from pages.base_page import BasePage


class AgentsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = "/agents/overview"
        self.unauthorized_agents_selector = "[data-test-agents-sidebar-title] >> text='UNAUTHORIZED AGENTS'"
        self.authorize_button_selector = "button[data-test-authorize-agent]"
        self.authorize_button_at_popup_selector = "[data-portaltarget] button.ring-button-primary"

    @allure.step("Переход на страницу агентов и авторизация нового неавторизованного агента")
    def authorize_agent(self):
        self.actions.navigate(self.page_url)
        self.actions.wait_for_url_change(self.page_url)
        self.actions.click_button(self.unauthorized_agents_selector)
        self.actions.click_button(self.authorize_button_selector)
        self.actions.click_button(self.authorize_button_at_popup_selector)