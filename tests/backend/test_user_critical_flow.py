import pytest
import allure
import time
from data.project_data import ProjectResponseModel
from data.build_conf_data import BuildResponseModel
from data.run_build_data import BuildRunResponseModel, BuildConfRunStatusModel


class TestProjectCreate:

    @allure.feature("Project and build configuration management")
    @allure.story(
        "Create a project and building a configuration with subsequent launch for it under different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case")
    @allure.title(
        "Check the user flow for creating a project, building a configuration and launching it"
    )
    @allure.description(
        "The test checks the creation of a new project and its appearance in the general list of projects."
    )
    def test_user_critical_flow_with_roles(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data,
        build_conf_run_data,
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert (
                project_model_response.id == project_data_1.id
            ), f"expected project id= {project_data_1.id}, but '{project_model_response.id}' given"
        with pytest.assume:
            assert (
                project_model_response.parentProjectId == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Check if the created project id is in the general list of projects"
        ):
            get_project_response = (
                super_admin.api_manager.project_api.get_project_by_locator(
                    project_data_1.id).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            created_model_project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert (
                created_model_project_response.id == project_data_1.id
            ), f"There is no project with {project_data_1.id} id"
        with allure.step("Submit a request to create a build configuration"):
            build_conf_data_1 = build_conf_data
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()).text
            )
        with allure.step(
            "Check whether the parameters of the created build configuration match the sent data"
        ):
            build_conf_model_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert build_conf_model_response.id == build_conf_data_1.id, (
                f"expected build conf id= {build_conf_data_1.id},"
                f" but '{build_conf_model_response.id}' given"
            )
        with allure.step(
            "Check if the created build configuration id is in the general list of build configurations"
        ):
            get_build_conf_response = (
                super_admin.api_manager.build_conf_api.get_build_conf(
                    build_conf_data_1.id).text
            )
        with allure.step(
            "Check whether the parameters of the created build configuration match the sent data"
        ):
            build_conf_model_response_1 = BuildResponseModel.model_validate_json(
                get_build_conf_response
            )
        with pytest.assume:
            assert build_conf_model_response_1.id == build_conf_data_1.id, (
                f"expected build conf id= {build_conf_data_1.id},"
                f" but '{build_conf_model_response_1.id}' given"
            )
        with allure.step("Send a request to run the created build configuration"):
            build_conf_run_data_1 = build_conf_run_data
            build_run_response = (
                super_admin.api_manager.run_build_conf_api.run_build_conf(
                    build_conf_run_data_1.model_dump()).text
            )
            time.sleep(20)
        with allure.step(
            "Checking the compliance of the parameters of the build config launch model"
        ):
            build_run_model_response = BuildRunResponseModel.model_validate_json(
                build_run_response
            )
        with pytest.assume:
            assert build_run_model_response.state == "queued", (
                f"build was expected to be run= {build_run_model_response.state} should be queued,"
                f" but it is not in a query= {build_run_model_response.state}"
            )
        with allure.step(
            "Send a request to check the number of build configurations in the queue to run"
        ):
            get_build_conf_run_response = (
                super_admin.api_manager.build_conf_api.check_query_with_build_conf().text
            )
            time.sleep(15)
        with allure.step(
            "Check the compliance of the parameters of the build configuration launch response model with the sent data"
        ):
            build_run_response = BuildConfRunStatusModel.model_validate_json(
                get_build_conf_run_response
            )
        with pytest.assume:
            assert (
                build_run_response.count == 0
            ), f"build was expected to be out of the query=0, but it is still here: query={build_run_response.count}"
