from http import HTTPStatus
import allure
import pytest
from data.build_conf_data import BuildResponseModel
from data.project_data import ProjectResponseModel
from pages.create_project_page import ProjectCreationPage
from pages.edit_build_conf_page import BuildConfEditPage
from pages.login_page import LoginPage
from pages.edit_project_page import EditProjectFormPage
from pages.create_build_conf_page import BuildConfCreationPage
from pages.welcome_page import CreateTheFirstProjectPage
from resources.user_creds import UsualUserCreds
from utilis.data_generator import DataGenerator


@allure.feature("Manage build configurations")
@allure.story("Creatie a build configuration with invalid data")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Documentation")
@allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
@allure.testcase("https://testcase.manager/testcase/1", name="Test-case-204")
@allure.title(
    "Checking creation of build configuration with empty mandatory fields, "
    " invalid id, with already existing build configuration name"
)
@allure.description(
    "Negative test checks creation of build configuration with empty"
    " required fields, invalid id, with already existing"
    " build configuration name."
)
def test_create_build_conf_with_invalid_data(browser, project_data, super_admin, build_conf_data, delete_all_projects):
    project_data_1 = project_data
    project_id = project_data_1.id
    project_name = project_data_1.name
    build_conf_data_1 = build_conf_data
    build_conf_id = build_conf_data_1.id
    build_conf_name = build_conf_data_1.name
    description = DataGenerator.random_text()
    invalid_build_id = DataGenerator.incorrect_id_1()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("User authorization"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
        login_browser.check_url_favourite_projects()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Create the first project"):
        fst_project_creation_brw = CreateTheFirstProjectPage(browser)
        fst_project_creation_brw.tap_on_create_first_project()
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.create_project_manually(
            project_name, project_id, description
        )
        project_creation_browser.check_url_after_prt_crt(project_id)
    with allure.step("Check redirect on project edit page"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description
        )
    with allure.step("Go to the build configuration creation page"):
        edit_project_browser.redirect_to_create_build_conf(project_id)
        with allure.step(
            "Send a request to receive information about the created project"
        ):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_data_1.id
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
    with allure.step("Create a build configuration"):
        build_conf_creation_browser = BuildConfCreationPage(browser, project_id)
        build_conf_creation_browser.create_build_conf(
            build_conf_id, build_conf_name, description
        )
        build_conf_creation_browser.check_url_after_build_create(
            build_conf_id, project_id
        )
    with allure.step(
        "Check if the created build configuration id is in the general list of build configurations"
    ):
        get_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(
            build_conf_data_1.id
        ).text
    with allure.step(
        "Check whether the parameters of the created build configuration match the sent data"
    ):
        build_conf_model_response_1 = BuildResponseModel.model_validate_json(
            get_build_conf_response
        )
        assert build_conf_model_response_1.id == build_conf_data_1.id, (
            f"expected build conf id= {build_conf_data_1.id},"
            f" but '{build_conf_model_response_1.id}' given"
        )
    with allure.step("Create a build configuration with empty name and id fields"):
        build_conf_error = BuildConfCreationPage(browser, project_id)
        build_conf_error.create_build_conf(" ", " ", description)
        build_conf_error.check_error_empty_build_name()
        build_conf_error.check_error_empty_build_id()
    with allure.step("Create a build configuration with an invalid id"):
        build_conf_error.create_build_conf(
            invalid_build_id, build_conf_name, str(invalid_build_id[0])
        )
        build_conf_error.check_error_invalid_build_id(
            invalid_build_id, str(invalid_build_id[0])
        )
    with allure.step("Create a build configuration with an existing build name"):
        build_conf_error.create_build_conf(project_id, build_conf_name, project_name)
        build_conf_error.check_error_used_build_id(build_conf_name, project_name)
    with allure.step("Send a request to get build configuration information"):
        get_about_build_conf_response = (
            super_admin.api_manager.build_conf_api.get_build_conf(
                project_id, expected_status=HTTPStatus.NOT_FOUND
            )
        )
    with pytest.assume:
        assert (
            f"NotFoundException: No build type nor template is found"
            f" by id '{project_id}'"
        ) in get_about_build_conf_response.text


@allure.feature("Manage build configurations")
@allure.story("Create a copy of the build configuration")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Documentation")
@allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
@allure.testcase("https://testcase.manager/testcase/1", name="Test-case-205")
@allure.title(
    "Check the creation of a copy of the build configuration with a change in the build configuration id"
)
@allure.description(
    "A positive test checks for creating a copy of the build configuration with a change in the build configuration id."
)
def test_create_build_conf_by_copy(
    browser, project_data, super_admin, build_conf_data, project_data_first_project
):
    project_data_1 = project_data
    project_id = project_data_1.id
    project_name = project_data_1.name
    build_conf_data_1 = build_conf_data
    build_conf_id = build_conf_data_1.id
    build_conf_name = build_conf_data_1.name
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]
    new_build_conf_id = DataGenerator.fake_project_id()

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
    with allure.step("Creating a project"):
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
    with allure.step("Go to the build configuration creation page"):
        edit_project_browser.redirect_to_create_build_conf(project_id)
        with allure.step(
            "Send a request to receive information about the created project"
        ):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_data_1.id
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
    with allure.step("Create a build configuration"):
        build_conf_creation_browser = BuildConfCreationPage(browser, project_id)
        build_conf_creation_browser.create_build_conf(
            build_conf_id, build_conf_name, description
        )
        build_conf_creation_browser.check_url_after_build_create(
            build_conf_id, project_id
        )
    with allure.step("Check the display of the application build version"):
        build_conf_creation_browser.footer.check_build_version_is_visible()
    with allure.step("Check the display of the application name"):
        build_conf_creation_browser.footer.check_app_name_is_visible()
    with allure.step("Check the display of copywriting text"):
        build_conf_creation_browser.footer.check_copyright_text_is_visible()
    with allure.step(
        "Check if the created build configuration id is in the general list of build configurations"
    ):
        get_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(
            build_conf_data_1.id
        ).text
    with allure.step(
        "Check whether the parameters of the created build configuration match the sent data"
    ):
        build_response_1 = BuildResponseModel.model_validate_json(
            get_build_conf_response
        )
        assert (
            build_response_1.id == build_conf_data_1.id
        ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response_1.id}' given"
    with allure.step("Copy build configuration"):
        edit_build_conf = BuildConfEditPage(browser, build_conf_id)
        edit_build_conf.copy_build_conf(new_build_conf_id, new_build_conf_id)
        edit_build_conf.check_success_message_build_copy(new_build_conf_id)
    with allure.step("Remove build configuration"):
        edit_build_conf.delete_build_conf(new_build_conf_id, project_id)
    with allure.step(
        "Send a request to get information about a remote build configuration"
    ):
        get_about_build_conf_response = (
            super_admin.api_manager.build_conf_api.get_build_conf(
                new_build_conf_id, expected_status=HTTPStatus.NOT_FOUND
            )
        )
    with pytest.assume:
        assert (
            f"NotFoundException: No build type nor template is found"
            f" by id '{new_build_conf_id}'"
        ) in get_about_build_conf_response.text


@allure.feature("Manage build configurations")
@allure.story("Create a copy of the build configuration with invalid data")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Documentation")
@allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
@allure.testcase("https://testcase.manager/testcase/1", name="Test-case-206")
@allure.title("Check for creation of a copy of a build configuration with an invalid id")
@allure.description(
    "Negative test checks for creating a copy of a build configuration with an invalid id."
)
def test_create_invalid_copy_build_conf(
    browser,
    project_data,
    super_admin,
    build_data_without_del_id,
    project_data_first_project,
):
    project_data_1 = project_data
    project_id = project_data_1.id
    project_name = project_data_1.name
    build_conf_data_1 = build_data_without_del_id
    build_conf_id = build_conf_data_1.id
    build_conf_name = build_conf_data_1.name
    description = DataGenerator.random_text()
    invalid_build_id = DataGenerator.incorrect_id_1()
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
    with allure.step("Creating a project"):
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
    with allure.step("Go to the build configuration creation page"):
        edit_project_browser.redirect_to_create_build_conf(project_id)
        with allure.step(
            "Send a request to receive information about the created project"
        ):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_data_1.id
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
    with allure.step("Create a build configuration"):
        build_conf_creation_browser = BuildConfCreationPage(browser, project_id)
        build_conf_creation_browser.create_build_conf(
            build_conf_id, build_conf_name, description
        )
        build_conf_creation_browser.check_url_after_build_create(
            build_conf_id, project_id
        )
    with allure.step(
        "Check if the created build configuration id is in the general list of build configurations"
    ):
        get_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(
            build_conf_data_1.id
        ).text
    with allure.step(
        "Check whether the parameters of the created build configuration match the sent data"
    ):
        build_conf_model_response_1 = BuildResponseModel.model_validate_json(
            get_build_conf_response
        )
        assert build_conf_model_response_1.id == build_conf_data_1.id, (
            f"expected build conf id= {build_conf_data_1.id},"
            f" but '{build_conf_model_response_1.id}' given"
        )
    with allure.step("Copy build configuration with invalid id"):
        edit_build_conf = BuildConfEditPage(browser, build_conf_id)
        edit_build_conf.copy_build_conf(invalid_build_id, build_conf_name)
        edit_build_conf.check_error_message_build_copy(
            invalid_build_id, str(invalid_build_id[0])
        )
    with allure.step("Remove build configuration"):
        edit_build_conf.delete_build_conf(build_conf_name, project_id)
    with allure.step(
        "Send a request to get information about a remote build configuration"
    ):
        get_about_build_conf_response = (
            super_admin.api_manager.build_conf_api.get_build_conf(
                project_id, expected_status=HTTPStatus.NOT_FOUND
            )
        )
    with pytest.assume:
        assert (
            f"NotFoundException: No build type nor template is found by id"
            f" '{project_id}'"
        ) in get_about_build_conf_response.text
