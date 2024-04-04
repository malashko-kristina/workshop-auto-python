import allure
from pages.base_page import BasePage


class MsgBuildConfCreatedFrt(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.message_created_build = ("#unprocessed_buildType"
                                      "Created")

    def check_text_in_selector(self):
        with allure.step("Проверка наличия текста на странице"):
            self.actions.assert_text_in_element(
                self.message_created_build,
                "Build configuration successfully created."
                " You can now configure VCS roots.",
            )


class AddVCSPageFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_skip = '.cancel >> text="Skip"'

    def click_skip_vcs_add_button(self):
        with allure.step("Нажатие кнопки пропуска создания vcs"):
            self.actions.is_button_active(self.project_skip)
            self.actions.click_button(self.project_skip)


class AddVCSFormPage(BasePage):
    def __init__(self, page, build_conf_id, project_id):
        super().__init__(page)
        self.page_url = (f"/admin/editVcsRoot.html?action="
                         f"addVcsRoot&editingScope=buildType%3A"
                         f"{build_conf_id}&cameFromUrl=%2Fadmin%2Fedit"
                         f"BuildTypeVcsRoots.html%3Finit%3D1%26id%"
                         f"3DbuildType%3A{build_conf_id}d%26cameFromUrl"
                         f"%3D%252Fadmin%252FeditProject.html%253Finit%"
                         f"253D1%2526projectId%253D{project_id}&cameFrom"
                         f"Title=Version%20Control%20Settings&showSkip=true")
        self.message_created_build_conf = MsgBuildConfCreatedFrt(page)
        self.add_vcs_page = AddVCSPageFragment(page)

    def go_to_vcs_add_page(self):
        with allure.step("Переход на страницу добавления vcs"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def skip_vcs(self, build_conf_id, project_id):
        with allure.step(
            "Текст об успешном добавлении шагов к билд конфигурации"
        ):
            self.message_created_build_conf.check_text_in_selector()
        with allure.step("Клик по кнопке для пропуска секции VCS"):
            self.add_vcs_page.click_skip_vcs_add_button()
        with allure.step("Проверка загрузки страницы"):
            self.page_url = (f"/admin/editBuildTypeVcsRoots.html"
                             f"?init=1&id=buildType:{build_conf_id}"
                             f"&cameFromUrl=%2Fadmin%2FeditProject."
                             f"html%3Finit%3D1%26projectId%3D{project_id}")
            self.actions.wait_for_url_change(self.page_url)
