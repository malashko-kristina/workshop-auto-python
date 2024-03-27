import time

from actions.page_actions import PageAction


class Headers:
    def __init__(self, actions: PageAction):
        self.actions = actions
        self.logo_button = '.ring-icon-icon'
        self.project_button = 'a[title="Projects"] >> text="Projects"'
        self.add_project_button = 'a[title="Create subproject"][data-test-link-with-icon="add"]'
        self.changes_button = 'a[title="Changes"] >> text="Changes"'
        self.agents_button = 'a[title="Agents"][data-test="ring-link"]'
        self.agents_count = '.Links__counter--Bn[data-hint-container-id="header-agents-active"]'
        self.queue_button = 'a[title="Queue"][data-test="ring-link"]'
        self.queue_count = '..Links__counter--Bn[data-hint-container-id="header-queue-number"]'
        self.theme_drop_down = 'span.ring-button-content'
        self.light_theme = '.ring-list-label[title="Light"][data-test="ring-list-item-label"]'
        self.dark_theme = '.ring-list-label[title="Dark"][data-test="ring-list-item-label"]'
        self.system_theme = '.ring-list-label[title="System theme"][data-test="ring-list-item-label"]'
        self.administration_button = 'a[title="Administration"][data-test="ring-link"] >> text="Administration"'
        self.help_icon = '#userPanel > div:nth-child(5) > div > button'
        self.documentation_button = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text ="Documentation"'
        self.teamcity_kotlin = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text ="TeamCity Kotlin DSL"'
        self.feedback = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text ="Feedback"'
        self.getting_started = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text ="Getting started"'
        self.about_sakura = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text ="About Sakura UI"'
        self.whats_new = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text ="What\'s new"'
        self.search_button = "#SAKURA_HEADER_RIGHT > div > div > span"
        self.admin_button = 'button[title="admin"][type="button"]'
        self.profile_button = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text="Profile"'
        self.favourite_builds_button = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text="Favorite Builds"'
        self.investigation_button = 'a[data-test="ring-link ring-list-link ring-list-item"] >> text="Investigations"'
        self.logout_button = '.ring-link-inner >> text="Logout"'


    def logo_is_visible_and_clickable(self):
        self.actions.is_button_active(self.logo_button)
        self.actions.click_button(self.logo_button)
        self.actions.wait_for_page_load()

    def go_to_projects_through_header_button(self):
        self.actions.is_button_active(self.project_button)
        self.actions.click_button(self.project_button)
        self.actions.wait_for_page_load()

    def go_to_create_projects_through_header_button(self):
        self.actions.is_button_active(self.add_project_button)
        self.actions.click_button(self.add_project_button)
        self.actions.wait_for_page_load()
        self.actions.check_url(f"/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects", equal=False)


    def go_to_changes_through_header_button(self):
        self.actions.is_button_active(self.changes_button)
        self.actions.click_button(self.changes_button)
        self.actions.wait_for_page_load()

    def go_to_agents_through_header_button(self):
        self.actions.is_button_active(self.agents_button)
        self.actions.click_button(self.agents_button)
        self.actions.wait_for_page_load()

    def check_agents_count_through_header_button(self, number):
        self.actions.is_element_visible(self.agents_count)
        self.actions.assert_text_in_element(self.agents_count, number)

    def go_to_queue_through_header_button(self):
        self.actions.is_button_active(self.queue_button)
        self.actions.click_button(self.queue_button)
        self.actions.wait_for_page_load()

    def check_queue_count_through_header_button(self, number):
        self.actions.wait_for_selector(self.agents_count)
        self.actions.is_element_visible(self.agents_count)
        self.actions.assert_text_in_element(self.agents_count, number)
        time.sleep(30)

    def open_drop_down_theme_in_header_button(self):
        self.actions.is_button_active(self.theme_drop_down)
        self.actions.click_button(self.theme_drop_down)
        self.actions.wait_for_page_load()

    def change_theme_to_system(self):
        self.actions.wait_for_selector(self.theme_drop_down)
        self.actions.click_button(self.theme_drop_down)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.system_theme)
        self.actions.click_button(self.system_theme)
        self.actions.wait_for_page_load()

    def change_theme_to_light(self):
        self.actions.wait_for_selector(self.theme_drop_down)
        self.actions.click_button(self.theme_drop_down)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.light_theme)
        self.actions.click_button(self.light_theme)
        self.actions.wait_for_page_load()

    def change_theme_to_dark(self):
        self.actions.wait_for_selector(self.theme_drop_down)
        self.actions.click_button(self.theme_drop_down)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.dark_theme)
        self.actions.click_button(self.dark_theme)
        self.actions.wait_for_page_load()

    def go_to_administration_through_header_button(self):
        self.actions.is_button_active(self.administration_button)
        self.actions.click_button(self.administration_button)
        self.actions.wait_for_page_load()

    def go_to_help_through_header_button(self):
        self.actions.wait_for_selector(self.help_icon)
        self.actions.click_button(self.help_icon)
        self.actions.wait_for_page_load()

    def go_to_documentation_through_header_button(self):
        self.actions.is_button_active(self.help_icon)
        self.actions.click_button(self.help_icon)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.documentation_button)
        self.actions.click_button(self.documentation_button)
        self.actions.wait_for_page_load()

    def go_to_teamcity_kotlin_through_header_button(self):
        self.actions.is_button_active(self.help_icon)
        self.actions.click_button(self.help_icon)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.teamcity_kotlin)
        self.actions.click_button(self.teamcity_kotlin)
        self.actions.wait_for_page_load()

    def go_to_feedback_through_header_button(self):
        self.actions.is_button_active(self.help_icon)
        self.actions.click_button(self.help_icon)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.feedback)
        self.actions.click_button(self.feedback)
        self.actions.wait_for_page_load()

    def go_to_getting_started_through_header_button(self):
        self.actions.is_button_active(self.help_icon)
        self.actions.click_button(self.help_icon)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.getting_started)
        self.actions.click_button(self.getting_started)
        self.actions.wait_for_page_load()


    def go_to_about_sakura_through_header_button(self):
        self.actions.is_button_active(self.help_icon)
        self.actions.click_button(self.help_icon)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.about_sakura)
        self.actions.click_button(self.about_sakura)
        self.actions.wait_for_page_load()

    def go_to_whats_new_through_header_button(self):
        self.actions.is_button_active(self.help_icon)
        self.actions.click_button(self.help_icon)
        self.actions.wait_for_page_load()
        self.actions.is_button_active(self.whats_new)
        self.actions.click_button(self.whats_new)
        self.actions.wait_for_page_load()

    def open_search_field_through_header_button(self):
        self.actions.is_button_active(self.search_button)
        self.actions.click_button(self.search_button)
        self.actions.wait_for_page_load()

    def open_admin_panel_through_header_button(self):
        self.actions.is_button_active(self.admin_button)
        self.actions.click_button(self.admin_button)
        self.actions.wait_for_page_load()

    def go_to_profile_admin_panel_through_header_button(self):
        self.actions.is_button_active(self.admin_button)
        self.actions.click_button(self.admin_button)
        self.actions.wait_for_page_load()
        self.actions.wait_for_selector(self.profile_button)
        self.actions.click_button(self.profile_button)
        self.actions.wait_for_page_load()

    def go_to_favbuilds_admin_panel_through_header_button(self):
        self.actions.is_button_active(self.admin_button)
        self.actions.click_button(self.admin_button)
        self.actions.wait_for_page_load()
        self.actions.wait_for_selector(self.favourite_builds_button)
        self.actions.click_button(self.favourite_builds_button)
        self.actions.wait_for_page_load()

    def go_to_investigations_admin_panel_through_header_button(self):
        self.actions.is_button_active(self.admin_button)
        self.actions.click_button(self.admin_button)
        self.actions.wait_for_page_load()
        self.actions.wait_for_selector(self.investigation_button)
        self.actions.click_button(self.investigation_button)
        self.actions.wait_for_page_load()

    def go_to_logout_admin_panel_through_header_button(self):
        self.actions.is_button_active(self.admin_button)
        self.actions.click_button(self.admin_button)
        self.actions.wait_for_page_load()
        self.actions.wait_for_selector(self.logout_button)
        self.actions.click_button(self.logout_button)
        self.actions.wait_for_page_load()