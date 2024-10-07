import copy
import time
from http import HTTPStatus
import pytest
import allure
from data.project_data import ProjectResponseModel
from data.build_conf_data import BuildResponseModel
from data.run_build_data import (
    BuildRunResponseModel,
    BuildConfRunStatusModel,
)


class TestRunBuildConfSeveralTimes:

    @allure.feature("Manage the launch of build configurations")
    @allure.story(
        "Send a request to run the same build configuration multiple times with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-23")
    @allure.title("Check if the same build configuration is run multiple times")
    @allure.description(
        "The test checks the launch of the same build configuration several times."
    )
    def test_run_build_conf_several_times_with_roles(
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
        with allure.step("Send a request to run a build configuration"):
            build_conf_run_data_1 = build_conf_run_data
            build_run_response = (
                super_admin.api_manager.run_build_conf_api.run_build_conf(
                    build_conf_run_data_1.model_dump()).text
            )
            time.sleep(20)
        with allure.step(
            "Check whether the parameters of the running build configuration match the sent data"
        ):
            build_run_model_response = BuildRunResponseModel.model_validate_json(
                build_run_response
            )
        with pytest.assume:
            assert build_run_model_response.state == "queued", (
                f"build was expected to be run= {build_run_model_response.state} should be queued,"
                f" but it is not in a query= {build_run_model_response.state}"
            )
        with allure.step("Check the number of build configurations in the queue to run"):
            get_build_conf_run_response = (
                super_admin.api_manager.run_build_conf_api.check_query_with_build_conf().text
            )
        with allure.step(
            "Check the compliance of the parameters of the launched build configurations with the sent data"
        ):
            build_conf_run_check_model_response = (
                BuildConfRunStatusModel.model_validate_json(get_build_conf_run_response)
            )
        with pytest.assume:
            assert build_conf_run_check_model_response.count == 0, (
                f"build was expected to be out of the query=0,"
                f" but it is still here:"
                f" query={build_conf_run_check_model_response.count}"
            )
        with allure.step("Send a request to re-run the build configuration"):
            build_conf_run_data_2 = copy.deepcopy(build_conf_run_data)
            build_run_response = (
                super_admin.api_manager.run_build_conf_api.run_build_conf(
                    build_conf_run_data_2.model_dump()).text
            )
            time.sleep(20)
        with allure.step(
            "Check whether the parameters of the running build configuration match the sent data"
        ):
            build_run_model_response = BuildRunResponseModel.model_validate_json(
                build_run_response
            )
        with pytest.assume:
            assert build_run_model_response.state == "queued", (
                f"build was expected to be run= {build_run_model_response.state}"
                f" should be queued, but it is not in a query= {build_run_model_response.state}"
            )
        with allure.step(
            "Check whether the parameters of the running build configuration match the sent data"
        ):
            get_build_conf_run_response = (
                super_admin.api_manager.run_build_conf_api.check_query_with_build_conf().text
            )
            time.sleep(20)
        with allure.step(
            "Check the compliance of the parameters of the launched build configurations with the sent data"
        ):
            build_conf_run_check_model_response = (
                BuildConfRunStatusModel.model_validate_json(get_build_conf_run_response)
            )
        with pytest.assume:
            assert build_conf_run_check_model_response.count == 0, (
                f"build was expected to be out of the query=0,"
                f" but it is still here: query={build_conf_run_check_model_response.count}"
            )


class TestRunBuildConfWithWrongBuildConfId:

    @allure.feature("Manage the launch of build configurations")
    @allure.story(
        "Send a request to run a non-existent build configuration with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-24")
    @allure.title("Проверка запуска несуществующей билд конфигурации")
    @allure.description(
        "A negative test checks for running a non-existent build configuration.."
    )
    def test_run_build_conf_with_wrong_build_id_with_roles(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data,
        build_conf_run_data_with_wrong_build_conf_id,
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
            assert project_model_response.id == project_data_1.id, (
                f"expected project id= {project_data_1.id},"
                f" but '{project_model_response.id}' given"
            )
        with pytest.assume:
            assert (
                project_model_response.parentProjectId == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
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
        with allure.step("Send a request to run a build configuration"):
            build_conf_run_data_1 = build_conf_run_data_with_wrong_build_conf_id
            build_run_response = (
                super_admin.api_manager.run_build_conf_api.run_build_conf(
                    build_conf_run_data_1.model_dump(),
                    expected_status=HTTPStatus.NOT_FOUND,).text
            )
        with pytest.assume:
            assert (
                f"NotFoundException: No build type nor template is found by id"
                f" '{build_conf_run_data_1.buildType.id}'"
            ) in build_run_response
