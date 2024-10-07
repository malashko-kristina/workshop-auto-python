import copy
from http import HTTPStatus
import pytest
import allure
from data.project_data import ProjectResponseModel
from utilis.data_generator import DataGenerator


class TestProjectCreateWithInvalidData:

    @allure.feature("Project Management")
    @allure.story(
        'Send a request to create a project with an empty "id" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/1", name="Test-case-1")
    @allure.title('Check  if a project is created with an empty "id" field')
    @allure.description(
        'Negative test checks creation of a new project with empty "id" field.'
    )
    def test_create_project_with_empty_id(
        self, super_admin, user_create, project_data_with_empty_id
    ):
        with allure.step("Send a request to create a project with an empty id"):
            invalid_project_data = project_data_with_empty_id()
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    invalid_project_data.model_dump(),
                    expected_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            )

        with pytest.assume:
            assert (
                "InvalidIdentifierException: Project ID must not be empty"
                in create_project_response.text
            )

    @allure.feature("Project Management")
    @allure.story(
        'Send a request to create a project with invalid data in the "id" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-2")
    @allure.title('Check for project creation with invalid data in the "id" field')
    @allure.description(
        'Negative test checks creation of a new project with invalid data in the "id" field.'
    )
    def test_create_project_with_invalid_ids(
        self, super_admin, user_create, project_data_with_invalid_ids
    ):

        with allure.step(
            "Send a request to create a project with an invalid 'id' field"
        ):
            invalid_project_data = project_data_with_invalid_ids
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    invalid_project_data.model_dump(),
                    expected_status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )
            )

        with pytest.assume:
            assert (
                "ID should start with a latin letter and contain only latin letters,"
                " digits and underscores (at most 225 characters)"
                in create_project_response.text
            )

    @allure.feature("Project Management")
    @allure.story(
        'Send a request to create a project with an empty "name" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/1", name="Test-case-3")
    @allure.title('Check if a project is created with an empty "name" field')
    @allure.description(
        'The negative test checks the creation of a new project with an empty "name" field..'
    )
    def test_create_project_with_empty_name(
        self, super_admin, user_create, project_data_with_invalid_name
    ):

        with allure.step("Submit a request to create a project with an empty 'name' field"):
            invalid_project_data = project_data_with_invalid_name()
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    invalid_project_data.model_dump(),
                    expected_status=HTTPStatus.BAD_REQUEST,
                )
            )

        with pytest.assume:
            assert (
                "BadRequestException: Project name cannot be empty"
                in create_project_response.text
            )

    @allure.feature("Project Management")
    @allure.story(
        'Send a request to create a project with an empty "parentProject" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/1", name="Test-case-4")
    @allure.title('Check if a project is created with an empty "parentProject" field')
    @allure.description(
        'Negative test checks creation of a new project with empty "parentProject" field.'
    )
    def test_create_project_with_empty_parentProject(
        self, super_admin, user_create, project_data_with_empty_parentProject
    ):

        with allure.step(
            "Send a request to create a project with an empty 'parentProject' field"
        ):
            invalid_project_data = project_data_with_empty_parentProject()
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    invalid_project_data.model_dump(),
                    expected_status=HTTPStatus.BAD_REQUEST,
                )
            )

        with pytest.assume:
            assert (
                "BadRequestException: No project specified. Either 'id', 'internalId' or 'locator' attribute should be present"
                in create_project_response.text
            )

    @allure.feature("Project Management")
    @allure.story(
        'Send a request to create a project with invalid data in the "parentProject" field with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-5")
    @allure.title(
        'Check for project creation with invalid data in the "parentProject" field'
    )
    @allure.description(
        'Negative test checks creation of a new project with invalid data in the "parentProject" field.'
    )
    def test_create_project_with_invalid_parentProject(
        self, super_admin, user_create, project_data_with_invalid_parentProject
    ):

        with allure.step(
            "Send a request to create a project with invalid data in the 'parentProject' field"
        ):
            invalid_project_data = project_data_with_invalid_parentProject
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    invalid_project_data.model_dump(),
                    expected_status=HTTPStatus.NOT_FOUND,
                )
            )

        with pytest.assume:
            assert (
                "NotFoundException: No project found by name or internal/external id"
                in create_project_response.text
            )


class TestProjectCreateWithVariantData:

    @allure.feature("Project Management")
    @allure.story(
        'Send request to create project with boolean value "False" in "copyAllAssociatedSettings" with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-6")
    @allure.title(
        'Check if project is created with boolean value "False" in "copyAllAssociatedSettings"'
    )
    @allure.description(
        'The test checks the creation of a new project with a boolean value of "False" in "copyAllAssociatedSettings".'
    )
    def test_create_project_with_false(
        self, super_admin, user_create, project_data_with_false
    ):

        with allure.step(
            "Send a request to create a project with a boolean value of false in the 'copyAllAssociatedSettings' field"
        ):
            project_data_2 = project_data_with_false()
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_2.model_dump()
                ).text
            )
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

        with pytest.assume:
            assert (
                project_model_response.parentProjectId == project_data_2.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_2.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )


class TestProjectCreateWithTheSameData:

    @allure.feature("Project Management")
    @allure.story(
        'Send a request to create a project with an existing "name" of another project with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-7")
    @allure.title('Check if a project is created with an existing "name" of another project')
    @allure.description(
        'A negative test checks the creation of a new project with an existing "name" of another project".'
    )
    def test_create_project_when_project_exists_with_name(
        self, super_admin, user_create, project_data
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
        with allure.step(
            "Submit a request to create a project with the same name as the previous request"
        ):
            create_project_response_2 = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump(), expected_status=HTTPStatus.BAD_REQUEST
                )
            )
        with pytest.assume:
            assert (
                "DuplicateProjectNameException: Project with this name already exists"
                in create_project_response_2.text
            )

    @allure.feature("Project Management")
    @allure.story(
        'Submit a request to create a project with an existing "id" of another project with different roles'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-8")
    @allure.title('Check if a project is created with an existing "id" of another project')
    @allure.description(
        'A negative test checks the creation of a new project with an existing "id" of another project".'
    )
    def test_create_project_when_project_exists_with_id(
        self, super_admin, user_create, project_data
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step("Check the compliance of the parameters of the created project"):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert project_model_response.id == project_data_1.id, (
                f"expected project id= {project_data_1.id},"
                f" but '{project_model_response.id}' given"
            )
        with allure.step("Submit a request to create a project with the same id"):
            project_data_2 = copy.deepcopy(project_data_1)
            project_data_2.name = DataGenerator.fake_build_id()
            create_project_response_2 = (
                super_admin.api_manager.project_api.create_project(
                    project_data_2.model_dump(), expected_status=HTTPStatus.BAD_REQUEST
                )
            )
        with pytest.assume:
            assert (
                f"DuplicateExternalIdException:"
                f' Project ID "{project_data_1.id}" is already used by'
                f" another project"
            ) in create_project_response_2.text


class TestProjectCopy:

    @allure.feature("Project Management")
    @allure.story(
        "Submit a request to copy an existing project with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-9")
    @allure.title("Check if a project is copied from an existing project")
    @allure.description(
        'The test checks the creation of a new project based on an existing project by copying".'
    )
    def test_project_copy(
        self, super_admin, user_create, project_data, project_copy_data
    ):

        with allure.step("Submit a request to create a project"):
            project_data_3 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_3.model_dump()).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert project_model_response.id == project_data_3.id, (
                f"expected project id= {project_data_3.id},"
                f" but '{project_model_response.id}' given"
            )
        with pytest.assume:
            assert (
                project_model_response.parentProjectId == project_data_3.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_3.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Submit a request to create a copy of an existing project"
        ):
            project_copy_data_1 = project_copy_data
            create_project_copy_response = (
                super_admin.api_manager.project_api.create_copy_project(
                    project_copy_data_1.model_dump()).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_copy_model_response = ProjectResponseModel.model_validate_json(
                create_project_copy_response
            )
        with pytest.assume:
            assert project_copy_model_response.id == project_copy_data_1.id, (
                f"expected project id= {project_copy_data_1.id},"
                f" but '{project_copy_model_response.id}' given"
            )
        with pytest.assume:
            assert (
                project_copy_model_response.parentProjectId == project_copy_data_1.parentProject["locator"]
            ), (
                f"expected parent project id="
                f" {project_copy_data_1.parentProject['locator']},"
            )

    @allure.feature("Project Management")
    @allure.story(
        "Send a request to copy a project with an unknown project id with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-10")
    @allure.title("Check for copying a project with an unknown project id")
    @allure.description(
        'Negative test checks creation of new project by copying using non-existent project id".'
    )
    def test_project_copy_with_invalid_source_project(
        self,
        super_admin,
        user_create,
        project_data,
        project_copy_data_with_another_source_project,
    ):

        with allure.step("Submit a request to create a project"):
            project_data_3 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_3.model_dump()).text
            )
        with allure.step(
            "Check whether the parameters of the created project match the submitted data"
        ):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response
            )
        with pytest.assume:
            assert project_model_response.id == project_data_3.id, (
                f"expected project id= {project_data_3.id},"
                f" but '{project_model_response.id}' given"
            )
        with pytest.assume:
            assert (
                project_model_response.parentProjectId == project_data_3.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_3.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Submit a request to create a copy of an existing project, but with an unknown id specified"
        ):
            project_copy_data_2 = project_copy_data_with_another_source_project()
            create_project_copy_response = (
                super_admin.api_manager.project_api.create_copy_project(
                    project_copy_data_2.model_dump(),
                    expected_status=HTTPStatus.NOT_FOUND,
                )
            )
        with pytest.assume:
            assert (
                f"NotFoundException: No project found by name or internal/external"
                f" id '{project_copy_data_2.sourceProject['locator']}'"
            ) in create_project_copy_response.text


class TestProjectCreateAndDelete:

    @allure.feature("Project Management")
    @allure.story(
        "Send a request to get information about a remote project with different roles"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Documentation")
    @allure.issue("https://issue.tracker/project/123", name="Bug-tracker")
    @allure.testcase("https://testcase.manager/testcase/2", name="Test-case-11")
    @allure.title("Check a request for information about a remote project")
    @allure.description(
        'The test checks the creation of a new project, its deletion and obtaining'
        ' information about the deleted project".'
    )
    def test_create_project_and_delete(
        self, super_admin, user_create, project_data_without_deleting
    ):

        with allure.step("Submit a request to create a project"):
            project_data_1 = project_data_without_deleting()
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
        with allure.step("Send a request to delete a created project"):
            delete_project_response = (
                super_admin.api_manager.project_api.delete_project(
                    project_model_response.id
                )
            )
        with pytest.assume:
            assert delete_project_response.status_code == 204
        with allure.step(
            "Send a request for information about a remote project"
        ):
            get_delete_project_response = (
                super_admin.api_manager.project_api.get_project_by_locator(
                    project_model_response.id, expected_status=HTTPStatus.NOT_FOUND
                )
            )
        with pytest.assume:
            assert (
                f"NotFoundException: No project found by name or internal/external"
                f" id '{project_data_1.id}'"
            ) in get_delete_project_response.text
