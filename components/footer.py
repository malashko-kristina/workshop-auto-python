from actions.page_actions import PageAction
from resources.footer_info import BuildVersion, AppName

class Footers:
    def __init__(self, actions: PageAction):
        self.actions = actions
        self.app_name = AppName.app_name()
        self.build_version = BuildVersion.build_version()
        self.copyright_text = '.greyNote >> text="Copyright © 2006–2024 JetBrains s.r.o."'
        self.about_button = 'a[data-test="ring-link"] >> text="About TeamCity"'
        self.license_agreement_button = 'a[data-test="ring-link"] >> text="License Agreement"'



    def check_build_version_is_visible(self):
        self.actions.is_element_visible(self.build_version)


    def check_app_name_is_visible(self):
        self.actions.is_element_visible(self.app_name)


    def check_copyright_text_is_visible(self):
        self.actions.is_element_visible(self.copyright_text)
        self.actions.assert_text_in_element(self.copyright_text, "Copyright © 2006–2024 JetBrains s.r.o.")


    def go_to_about_teamcity_page(self):
        self.actions.wait_for_selector(self.about_button)
        self.actions.click_button(self.about_button)
        self.actions.wait_for_page_load()


    def go_to_license_agreement_page(self):
        self.actions.wait_for_selector(self.license_agreement_button)
        self.actions.click_button(self.license_agreement_button)
        self.actions.wait_for_page_load()