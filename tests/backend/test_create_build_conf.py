import copy
from http import HTTPStatus
import pytest
import allure
from data.project_data import ProjectResponseModel
from data.build_conf_data import BuildResponseModel
from utilis.data_generator import DataGenerator


class TestBuildCreateWithInvalidData:

    @allure.feature("Manage build configurations")
    @allure.story(
        'Sending a request to create a build configuration with an empty "id" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-12")
    @allure.title('Check the creation of a build configuration with an empty "id" field')
    @allure.description(
        'Negative test creating a build configuration with an empty "id" field.'
    )
    def test_create_build_conf_with_empty_id_field(
        self, super_admin, user_create, project_data, build_conf_data_with_empty_id
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
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
                    project_data_1.id
                ).text
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

        with allure.step(
            "Send a request to create a build configuration with an empty id field"
        ):
            build_conf_data_1 = build_conf_data_with_empty_id
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump(),
                    expected_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            )

        with pytest.assume:
            assert (
                "InvalidIdentifierException: Build configuration or template ID must not be empty"
                in build_config_response.text
            )

    @allure.story(
        'Send a request to create a build configuration with invalid data in the "id" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-13")
    @allure.title(
        'Check for creation of build configuration with invalid data in the "id" field'
    )
    @allure.description(
        'Negative test creating a build configuration with invalid data in the "id" field.'
    )
    def test_create_build_conf_with_invalid_id_field(
        self, super_admin, user_create, project_data, build_data_with_invalid_ids
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
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
        with pytest.assume:
            assert created_model_project_response.id == project_data_1.id, (
                f"There is no project with" f" {project_data_1.id} id"
            )
        with allure.step(
            "Send a request to create a build configuration with invalid data in the 'id' field"
        ):
            build_conf_data_1 = build_data_with_invalid_ids
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump(),
                    expected_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            )
        with pytest.assume:
            assert (
                "ID should start with a latin letter and contain only latin letters,"
                " digits and underscores (at most 225 characters)."
            ) in build_config_response.text

    @allure.story(
        'Send a request to create a build configuration with an empty "name" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-14")
    @allure.title('Check the creation of a build configuration with an empty "name" field')
    @allure.description(
        'Negative test creating a build configuration with an empty "name" field.'
    )
    def test_create_build_conf_with_empty_name_field(
        self, super_admin, user_create, project_data, build_conf_data_with_empty_name
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
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
        with pytest.assume:
            assert created_model_project_response.id == project_data_1.id, (
                f"There is no project" f" with {project_data_1.id} id"
            )
        with allure.step(
            "Send a request to create a build configuration with an empty 'name' field"
        ):
            build_conf_data_1 = build_conf_data_with_empty_name
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump(),
                    expected_status=HTTPStatus.BAD_REQUEST,
                )
            )
        with pytest.assume:
            assert (
                "BadRequestException: When creating a build type, non empty name should be provided"
                in build_config_response.text
            )

    @allure.story(
        'Send a request to create a build configuration with invalid data in the "project_id" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-15")
    @allure.title(
        'Check for creation of build configuration with invalid data in the "project_id" field'
    )
    @allure.description(
        'Negative test creating a build configuration with invalid data in the "project_id" field.'
    )
    def test_create_build_conf_with_invalid_project_id(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data_with_invalid_project_id,
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
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
            project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert (
                project_response.id == project_data_1.id
            ), f"There is no project with {project_data_1.id} id"
        with allure.step(
            "Send a request to create a build configuration with invalid data in the 'project_id' field"
        ):
            build_conf_data_1 = build_conf_data_with_invalid_project_id
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump(), expected_status=HTTPStatus.NOT_FOUND
                )
            )
        with pytest.assume:
            assert (
                f"NotFoundException: No project found by locator"
                f" 'count:1,id:{build_conf_data_1.project['id']}'."
                f" Project cannot be found by external id"
                f" '{build_conf_data_1.project['id']}"
            ) in build_config_response.text


class TestBuildConfCreateWithoutObligatoryFields:

    @allure.feature("Manage build configurations")
    @allure.story(
        'Send a request to create a build configuration with an empty "steps" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-16")
    @allure.title('Check the creation of a build configuration with an empty "steps" field')
    @allure.description(
        'The test checks the creation of a build configuration with an empty "steps" field.'
    )
    def test_create_build_conf_with_empty_steps_field(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data_with_empty_steps_field,
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert project_model_response.id == project_data_1.id, (
                f"expected project id= {project_data_1.id}, "
                f"but '{project_model_response.id}' given"
            )
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
                    project_data_1.id
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert project_response.id == project_data_1.id, (
                f"There is no project" f" with {project_data_1.id} id"
            )
        with allure.step(
            "Send a request to create a build configuration with an empty 'steps' field"
        ):
            build_conf_data_1 = build_conf_data_with_empty_steps_field()
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created build configuration match the sent data"
        ):
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )

        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"

    @allure.feature("Manage build configurations")
    @allure.story(
        'Send a request to create a build configuration without the "steps" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-17")
    @allure.title('Check the creation of a build configuration without the "steps" field')
    @allure.description('The test checks the creation of a build configuration without the "steps" field.')
    def test_create_build_conf_without_steps_field(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data_without_steps_field,
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert (
                project_response.id == project_data_1.id
            ), f"expected project id= {project_data_1.id}, but '{project_response.id}' given"
        with pytest.assume:
            assert (
                project_response.parentProjectId == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
            )
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
            project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert project_response.id == project_data_1.id, (
                f"There is no project with" f" {project_data_1.id} id"
            )
        with allure.step(
            "Send a request to create a build configuration without the 'steps' field"
        ):
            build_conf_data_1 = build_conf_data_without_steps_field()
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created build configuration match the sent data"
        ):
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"


class TestBuildConfCreateWithAlreadyUsedIdAndName:

    @allure.feature("Manage build configurations")
    @allure.story(
        "Send a request to create a build configuration with a name that is already in use, with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-18")
    @allure.title(
        'Check creation of build configuration with already existing "name" build configuration'
    )
    @allure.description(
        'Negative test checks creation of build configuration with already existing "name" build configuration.'
    )
    def test_create_build_conf_when_build_conf_exists_with_name(
        self, super_admin, user_create, project_data, build_conf_data
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
                f"but '{project_model_response.id}' given"
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
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"
        with allure.step(
            "Submit a request to create a build configuration с не уникальным 'name'"
        ):
            build_conf_data_2 = copy.deepcopy(build_conf_data)
            build_conf_data_2.id = DataGenerator.fake_project_id()
            build_config_response_2 = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_2.model_dump(),
                    expected_status=HTTPStatus.BAD_REQUEST,
                )
            )
        with pytest.assume:
            assert (
                f"DuplicateBuildTypeNameException:"
                f' Build configuration with name "{build_conf_data_2.name}"'
                f' already exists in project: "{project_data_1.name}"'
            ) in build_config_response_2.text

    @allure.feature("Manage build configurations")
    @allure.story(
        "Submit a request to create a build configuration с id, которое уже используется, с разными ролями"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-19")
    @allure.title(
        'Check for creation of a build configuration with an existing "id" of a build configuration'
    )
    @allure.description(
        'Negative test checks creation of build configuration with already existing "id" of build configuration.'
    )
    def test_create_build_conf_when_build_conf_exists_with_id(
        self, super_admin, user_create, project_data, build_conf_data
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert (
                project_response.id == project_data_1.id
            ), f"expected project id= {project_data_1.id}, but '{project_response.id}' given"
        with pytest.assume:
            assert (
                project_response.parentProjectId == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
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
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"
        with allure.step(
            "Submit a request to create a build configuration with non-unique 'id'"
        ):
            build_conf_data_2 = build_conf_data
            build_config_response_2 = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_2.model_dump(),
                    expected_status=HTTPStatus.BAD_REQUEST,
                ).text
            )
        with pytest.assume:
            assert (
                f"DuplicateExternalIdException: The build configuration"
                f' / template ID "{build_conf_data_2.id}" is already used by another'
                f" configuration or template"
            ) in build_config_response_2


class TestBuildConfCopy:

    @allure.feature("Manage build configurations")
    @allure.story(
        "Sending a request to copy an existing build configuration with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-20")
    @allure.title("Check the copying of the build configuration")
    @allure.description(
        'The test checks copying of the build configuration to the current project".'
    )
    def test_project_copy(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data,
        build_conf_data_copy,
    ):
        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert (
                project_response.id == project_data_1.id
            ), f"expected project id= {project_data_1.id}, but '{project_response.id}' given"
        with pytest.assume:
            assert (
                project_response.parentProjectId == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
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
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert build_response.id == build_conf_data_1.id, (
                f"expected build conf id="
                f" {build_conf_data_1.id},"
                f" but '{build_response.id}' given"
            )
        with allure.step(
            "Send a request to create a copy of an existing build configuration"
        ):
            build_conf_data_copy_1 = build_conf_data_copy
            copy_build_conf_response = (
                super_admin.api_manager.build_conf_api.create_build_conf_copy(
                    build_conf_data_copy_1.model_dump(), project_data_1.id
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created copy of the build configuration match the sent data"
        ):
            build_response = BuildResponseModel.model_validate_json(
                copy_build_conf_response
            )
        with pytest.assume:
            assert (
                build_response.id == build_conf_data_copy_1.id
            ), f"expected project id= {build_conf_data_copy_1.id}, but '{build_response.id}' given"
        with pytest.assume:
            assert (
                build_response.projectId == project_data_1.id
            ), f"expected parent project id={project_data_1.id}"

    @allure.story(
        "Send a request to copy an existing build config with an unknown source build conf with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-21")
    @allure.title(
        'Check the copying of the build configuration с неизвестным "id" source build conf'
    )
    @allure.description(
        'Negative test checks creation of build config by copying using unknown "id" source build config.'
    )
    def test_build_conf_copy_with_invalid_source_build_conf(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data,
        build_data_copy_invalid_parent_bc,
    ):
        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert (
                project_response.id == project_data_1.id
            ), f"expected project id= {project_data_1.id}, but '{project_response.id}' given"
        with pytest.assume:
            assert (
                project_response.parentProjectId == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
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
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert build_response.id == build_conf_data_1.id, (
                f"expected build"
                f" conf id= {build_conf_data_1.id},"
                f" but '{build_response.id}' given"
            )
        with allure.step(
            "Send a request to create a copy of an existing build configuration с неизвестным source build conf"
        ):
            build_copy_1 = build_data_copy_invalid_parent_bc
            copy_build_conf_response = (
                super_admin.api_manager.build_conf_api.create_build_conf_copy(
                    build_copy_1.model_dump(),
                    project_data_1.id,
                    expected_status=HTTPStatus.NOT_FOUND,
                )
            )
        with pytest.assume:
            assert (
                f"NotFoundException: No build type or template is found by id,"
                f" internal id or name '{build_copy_1.sourceBuildTypeLocator}'"
            ) in copy_build_conf_response.text


class TestBuildConfCreateDeleteAndGetInfo:

    @allure.feature("Manage build configurations")
    @allure.story(
        "Send a request to create, delete a build configuration and get information about it with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug tracker")
    @allure.testcase("https://testcase.manager/testcase/456", name="Test-case-22")
    @allure.title(
        "Check the creation, deletion of a build configuration and obtaining information about it"
    )
    @allure.description(
        "The negative test checks the creation of a build configuration,"
        " its deletion and the request for information about it."
    )
    def test_create_build_conf_delete_and_get_info(
        self,
        super_admin,
        user_create,
        project_data,
        build_data_without_del_id,
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
            project_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert (
                project_response.id == project_data_1.id
            ), f"expected project id= {project_data_1.id}, but '{project_response.id}' given"
        with pytest.assume:
            assert (
                project_response.parentProjectId == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
            )
        with allure.step("Submit a request to create a build configuration"):
            build_conf_data_1 = build_data_without_del_id
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()).text
            )
        with allure.step(
            "Check whether the parameters of the created build configuration match the sent data"
        ):
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"
        with allure.step("Отправка запроса на удаление билд конфигурации"):
            build_conf_delete_response = (
                super_admin.api_manager.build_conf_api.delete_build_conf(
                    build_response.id
                )
            )
        with pytest.assume:
            assert build_conf_delete_response.status_code == 204
        with allure.step(
            "Send a request to get information about a remote build configuration"
        ):
            get_about_delete_build_conf_response = (
                super_admin.api_manager.build_conf_api.get_build_conf(
                    build_response.id, expected_status=HTTPStatus.NOT_FOUND
                )
            )
        with pytest.assume:
            assert (
                f"NotFoundException: No build type nor template is found by id"
                f" '{build_conf_data_1.id}'"
            ) in get_about_delete_build_conf_response.text
