from playwright.sync_api import Page
from actions.page_actions import PageAction
from components.footer import Footers
from enums.host import BASE_URL
from components.header import Headers

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._base_url = BASE_URL
        self._endpoint = ""
        self.actions = PageAction(page)
        self.header = Headers(self.actions)
        self.footer = Footers(self.actions)

    @property
    def page_url(self):
        return self._base_url + self._endpoint

    @page_url.setter
    def page_url(self, endpoint):
        self._endpoint = endpoint















