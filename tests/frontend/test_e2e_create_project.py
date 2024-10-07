from http import HTTPStatus
import allure
import pytest
from data.project_data import ProjectResponseModel
from pages.create_project_page import ProjectCreationPage
from pages.edit_project_page import EditProjectFormPage
from pages.login_page import LoginPage
from pages.welcome_page import CreateTheFirstProjectPage
from resources.user_creds import UsualUserCreds
from utilis.data_generator import DataGenerator


@allure.feature("Project Management")
@allure.story("Create the first project")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Documentation")
@allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
@allure.testcase("https://testcase.manager/testcase/1", name="Test-case-199")
@allure.title("Check the creation of the first project")
@allure.description("Positive test checks Create the first project in the account.")
def test_create_the_first_project(
    browser,
    project_data_create,
    super_admin,
    project_data_without_deleting,
    delete_all_projects,
):
    project_data_1 = project_data_create()
    project_id = project_data_1.id
    project_name = project_data_1.name
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("User authorization"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD
        )
        login_browser.check_url_favourite_projects()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Create the first project"):
        go_to_first_project_creation_browser = CreateTheFirstProjectPage(browser)
        go_to_first_project_creation_browser.tap_on_create_first_project()
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.create_project_manually(
            project_name, project_id, description
        )
        project_creation_browser.check_url_after_prt_crt(project_id)
    with allure.step("Check the redirect to the project editing page"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description
        )
    with allure.step("Send a request to receive information about the created project"):
        response = super_admin.api_manager.project_api.get_project_by_locator(
            project_name
        ).text
        created_project = ProjectResponseModel.model_validate_json(response)
        with pytest.assume:
            assert (
                created_project.id == project_id
            ), f"expected project id = {project_id}, but '{created_project.id}' given"
        with pytest.assume:
            assert created_project.parentProjectId == project_parent, (
                f"expected parent project = {project_parent},"
                f" but '{created_project.parentProjectId}' given"
            )
    with allure.step("Check the display of the application name"):
        edit_project_browser.footer.check_app_name_is_visible()
    with allure.step("Check the display of copywriting text"):
        edit_project_browser.footer.check_copyright_text_is_visible()
    with allure.step("Logout from account"):
        edit_project_browser.header.go_to_logout_admin_panel_through_header_button()
    with allure.step(
        "Check if the created project id is in the general list of projects"
    ):
        get_project_response = (
            super_admin.api_manager.project_api.get_project_by_locator(
                project_data_1.id
            ).text
        )
    with allure.step(
        "Check whether the parameters of the created project match the submitted data"
    ):
        created_model_project_response = ProjectResponseModel.model_validate_json(
            get_project_response
        )
        assert created_model_project_response.id == project_data_1.id, (
            f"There is no project with" f" {project_data_1.id} id"
        )


@allure.feature("Project Management")
@allure.story('Create a project with an empty "id" field, with an already used id')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Documentation")
@allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
@allure.testcase("https://testcase.manager/testcase/1", name="Test-case-200")
@allure.title('Check if a project is created with an empty "id" field, with an already used id')
@allure.description(
    'Negative test flow checks creation of a new project with empty "id" field, with already used id.'
)
def test_create_project_invalid_id_name(browser, project_data_create, super_admin, project_data_first_project):
    project_data_1 = project_data_create()
    project_id = project_data_1.id
    project_name = project_data_1.name
    project_name_2 = DataGenerator.fake_build_id()
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Submit a request to Create the first project"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()
        ).text
    with allure.step(
        "Check whether the parameters of the created project match the submitted data"
    ):
        project_model_response = ProjectResponseModel.model_validate_json(
            create_project_response
        )
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, (
            f"expected project id= {project_data_2.id},"
            f" but '{project_model_response.id}' given"
        )
    with allure.step("User authorization"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD
        )
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Go to the project creation page via the header"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.header.go_to_create_projects_through_header_button()
    with allure.step("Create a project via header"):
        project_creation_browser.create_project_manually(
            project_name, project_id, description
        )
        project_creation_browser.check_url_after_prt_crt(project_id)
    with allure.step("Check the redirect to the project editing page"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description
        )
    with allure.step("Send a request to receive information about the created project"):
        response = super_admin.api_manager.project_api.get_project_by_locator(
            project_name
        ).text
        created_project = ProjectResponseModel.model_validate_json(response)
        with pytest.assume:
            assert (
                created_project.id == project_id
            ), f"expected project id = {project_id}, but '{created_project.id}' given"
        with pytest.assume:
            assert created_project.parentProjectId == project_parent, (
                f"expected parent project = {project_parent},"
                f" but '{created_project.parentProjectId}' given"
            )
    with allure.step("Create a project with an empty name"):
        project_creation_with_error_browser = ProjectCreationPage(browser)
        project_creation_with_error_browser.go_to_creation_page()
        project_creation_with_error_browser.create_project_manually(
            "", project_id, description
        )
        project_creation_with_error_browser.check_error_empty_project_name_is_visible()
    with allure.step("Create a project with an already used id"):
        project_creation_with_error_browser.create_project_manually(
            project_name_2, project_id, description
        )
        project_creation_with_error_browser.check_error_invalid_project_id_is_visible(
            project_id
        )
    with allure.step("Check the display of the application build version"):
        project_creation_with_error_browser.footer.check_build_version_is_visible()
    with allure.step("Check the display of the application name"):
        project_creation_with_error_browser.footer.check_app_name_is_visible()
    with allure.step("Check the display of copywriting text"):
        project_creation_with_error_browser.footer.check_copyright_text_is_visible()


@allure.feature("Project Management")
@allure.story(
    "Change project data using an invalid id and then changing it correctly"
)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Documentation")
@allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
@allure.testcase("https://testcase.manager/testcase/1", name="Test-case-201")
@allure.title(
    "Change project data using an invalid id and then changing it correctly"
)
@allure.description(
    "Flow from a negative test on changing a project with an invalid id followed by its correct change."
)
def test_create_project_invalid_id_edit(
    browser, project_data_without_deleting, super_admin, project_data_first_project
):
    project_data_1 = project_data_without_deleting()
    project_id = project_data_1.id
    project_name = project_data_1.name
    project_id_invalid = DataGenerator.incorrect_id_1()
    project_id_2 = DataGenerator.fake_build_id()
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Submit a request to Create the first project"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()
        ).text
    with allure.step(
        "Check whether the parameters of the created project match the submitted data"
    ):
        project_model_response = ProjectResponseModel.model_validate_json(
            create_project_response
        )
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, (
            f"expected project id= {project_data_2.id},"
            f" but '{project_model_response.id}' given"
        )
    with allure.step("User authorization"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD
        )
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Create a project"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(
            project_name, project_id, description
        )
    with allure.step("Check the redirect to the project editing page"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description
        )
        with allure.step(
            "Send a request to receive information about the created project"
        ):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_name
            ).text
            created_project = ProjectResponseModel.model_validate_json(response)
            with pytest.assume:
                assert created_project.id == project_id, (
                    f"expected project id = {project_id},"
                    f" but '{created_project.id}' given"
                )
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, (
                    f"expected parent project = {project_parent},"
                    f" but '{created_project.parentProjectId}' given"
                )
    with allure.step("Edit a project using an invalid id"):
        project_invalid_edit_browser = EditProjectFormPage(browser, project_id)
        project_invalid_edit_browser.check_project_url_edit()
        project_invalid_edit_browser.add_changes_to_project_data(
            project_name, project_id_invalid, description
        )
        project_invalid_edit_browser.check_warning_message_edit()
        project_invalid_edit_browser.tap_on_save_changes_button()
        project_invalid_edit_browser.check_error_message_invalid_project_id_edit(
            project_id_invalid
        )
    with allure.step("Edit a project using valid data"):
        project_edit_browser = EditProjectFormPage(browser, project_id)
        project_edit_browser.check_project_url_edit()
        project_edit_browser.add_changes_to_project_data(
            project_name, project_id_2, description
        )
        project_edit_browser.tap_on_save_changes_button()
        project_edit_browser.check_success_message_edit_saved()
    with allure.step("Delete a project"):
        delete_project_browser = EditProjectFormPage(browser, project_id_2)
        delete_project_browser.check_project_url_edit()
        delete_project_browser.delete_project()
    with allure.step("Send a request for information about a remote project"):
        get_delete_project_response = (
            super_admin.api_manager.project_api.get_project_by_locator(
                project_id_2, expected_status=HTTPStatus.NOT_FOUND
            )
        )
    with pytest.assume:
        assert (
            f"NotFoundException: No project found by name or internal/external id"
            f" '{project_id_2}'"
        ) in get_delete_project_response.text


@allure.feature("Project Management")
@allure.story("Create a copy of an existing project with a change in id")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Documentation")
@allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
@allure.testcase("https://testcase.manager/testcase/1", name="Test-case-202")
@allure.title("Check the creation of a copy of the project")
@allure.description(
    "A positive test verifies the creation of a new project based on copying from an existing one."
)
def test_create_project_by_copy(
    browser, project_data_create, super_admin, project_data_first_project
):
    project_data_1 = project_data_create()
    project_id = project_data_1.id
    project_name = project_data_1.name
    description = DataGenerator.random_text()
    project_id_new = DataGenerator.fake_build_id()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Submit a request to Create the first project"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()
        ).text
    with allure.step(
        "Check whether the parameters of the created project match the submitted data"
    ):
        project_model_response = ProjectResponseModel.model_validate_json(
            create_project_response
        )
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, (
            f"expected project id= {project_data_2.id},"
            f" but '{project_model_response.id}' given"
        )
    with allure.step("User authorization"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD
        )
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Create a project"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(
            project_name, project_id, description
        )
    with allure.step("Check the redirect to the project editing page"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description
        )
        with allure.step(
            "Send a request to receive information about the created project"
        ):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_name
            ).text
            created_project = ProjectResponseModel.model_validate_json(response)
            with pytest.assume:
                assert created_project.id == project_id, (
                    f"expected project id = {project_id},"
                    f" but '{created_project.id}' given"
                )
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, (
                    f"expected parent project = {project_parent},"
                    f" but '{created_project.parentProjectId}' given"
                )
    with allure.step("Create a copy of the project"):
        edit_project_browser.check_project_url_edit()
        edit_project_browser.copy_project(project_id_new)
        edit_project_browser.check_success_message_project_copy()
    with allure.step(
        "Check if the created project id is in the general list of projects"
    ):
        get_project_response = (
            super_admin.api_manager.project_api.get_project_by_locator(
                project_id_new
            ).text
        )
    with allure.step(
        "Check whether the parameters of the created project match the submitted data"
    ):
        project_response = ProjectResponseModel.model_validate_json(
            get_project_response
        )
    with pytest.assume:
        assert (
            project_response.id == project_id_new
        ), f"There is no project with {project_id_new} id"
    with allure.step("Delete a project"):
        delete_project_browser = EditProjectFormPage(browser, project_id_new)
        delete_project_browser.check_project_url_edit()
        delete_project_browser.delete_project()
    with allure.step("Send a request for information about a remote project"):
        get_delete_project_response = (
            super_admin.api_manager.project_api.get_project_by_locator(
                project_id_new, expected_status=HTTPStatus.NOT_FOUND
            )
        )
    with pytest.assume:
        assert (
            f"NotFoundException: No project found by name or internal/external id"
            f" '{project_id_new}'"
        ) in get_delete_project_response.text


@allure.feature("Project Management")
@allure.story("Create a copy of an existing project with an empty id")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Documentation")
@allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
@allure.testcase("https://testcase.manager/testcase/1", name="Test-case-203")
@allure.title('Check if a project copy is created with an empty "id" field')
@allure.description(
    'A negative test checks the creation of a copy of a new project with an empty "id" field..'
)
def test_create_project_by_copy_empty_id(
    browser, project_data_create, super_admin, project_data_first_project
):
    project_data_1 = project_data_create()
    project_id = project_data_1.id
    project_name = project_data_1.name
    description = DataGenerator.random_text()
    project_id_empty = " "
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Submit a request to Create the first project"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()
        ).text
    with allure.step(
        "Check whether the parameters of the created project match the submitted data"
    ):
        project_response = ProjectResponseModel.model_validate_json(
            create_project_response
        )
    with pytest.assume:
        assert (
            project_response.id == project_data_2.id
        ), f"expected project id= {project_data_2.id}, but '{project_response.id}' given"
    with allure.step("User authorization"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD
        )
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Create a project"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(
            project_name, project_id, description
        )
    with allure.step("Check the redirect to the project editing page"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description
        )
        with allure.step(
            "Send a request to receive information about the created project"
        ):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_name
            ).text
            created_project = ProjectResponseModel.model_validate_json(response)
            with pytest.assume:
                assert created_project.id == project_id, (
                    f"expected project id = {project_id},"
                    f" but '{created_project.id}' given"
                )
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, (
                    f"expected parent project = {project_parent},"
                    f" but '{created_project.parentProjectId}' given"
                )
    with allure.step("Attempt to create a copy of a project with an empty project id"):
        edit_project_browser.check_project_url_edit()
        edit_project_browser.copy_project(project_id_empty)
        edit_project_browser.check_error_message_project_copy()
    with allure.step("Send a request to get information about an uncreated project"):
        get_delete_project_response = (
            super_admin.api_manager.project_api.get_project_by_locator(
                project_id_empty, expected_status=HTTPStatus.NOT_FOUND
            )
        )
    with pytest.assume:
        assert (
            f"NotFoundException: No project found by name or internal/external id"
            f" '{project_id_empty}'"
        ) in get_delete_project_response.text
