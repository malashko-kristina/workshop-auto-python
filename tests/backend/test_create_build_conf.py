import copy
from http import HTTPStatus
import pytest
import allure
from data.project_data import ProjectResponseModel
from data.build_conf_data import BuildResponseModel
from utilis.data_generator import DataGenerator


class TestBuildCreateWithInvalidData:

    @allure.feature("Управление билд конфигурациями")
    @allure.story(
        'Отправка запроса на создание билд конфигурации с пустым полем "id" с разными ролями'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-12")
    @allure.title('Проверка создания билд конфигурации с пустым полем "id"')
    @allure.description(
        'Негативный тест создание билд конфигурации с пустым полем "id".'
    )
    def test_create_build_conf_with_empty_id_field(
        self, super_admin, user_create, project_data, build_conf_data_with_empty_id
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_model_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Проверка нахождения id созданного проекта в общем списке проектов"
        ):
            get_project_response = (
                super_admin.api_manager.project_api.get_project_by_locator(
                    project_data_1.id
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
        ):
            created_model_project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert (
                created_model_project_response.id == project_data_1.id
            ), f"There is no project with {project_data_1.id} id"

        with allure.step(
            "Отправка запроса на создание билд конфигурации с пустым id полем"
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
        'Отправка запроса на создание билд конфигурации с invalid data в поле "id" с разными ролями'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-13")
    @allure.title(
        'Проверка создания билд конфигурации с невалидными данными в поле "id"'
    )
    @allure.description(
        'Негативный тест создание билд конфигурации с невалидными с невалидными данными в поле "id.'
    )
    def test_create_build_conf_with_invalid_id_field(
        self, super_admin, user_create, project_data, build_data_with_invalid_ids
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_model_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Проверка нахождения id созданного проекта в общем списке проектов"
        ):
            get_project_response = (
                super_admin.api_manager.project_api.get_project_by_locator(
                    project_data_1.id
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
        ):
            created_model_project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert created_model_project_response.id == project_data_1.id, (
                f"There is no project with" f" {project_data_1.id} id"
            )
        with allure.step(
            "Отправка запроса на создание билд конфигурации с invalid данными в 'id' поле"
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
        'Отправка запроса на создание билд конфигурации с пустым полем "name" с разными ролями'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-14")
    @allure.title('Проверка создания билд конфигурации с пустым полем "name"')
    @allure.description(
        'Негативный тест создание билд конфигурации с пустым полем "name".'
    )
    def test_create_build_conf_with_empty_name_field(
        self, super_admin, user_create, project_data, build_conf_data_with_empty_name
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_model_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Проверка нахождения id созданного проекта в общем списке проектов"
        ):
            get_project_response = (
                super_admin.api_manager.project_api.get_project_by_locator(
                    project_data_1.id
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
        ):
            created_model_project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert created_model_project_response.id == project_data_1.id, (
                f"There is no project" f" with {project_data_1.id} id"
            )
        with allure.step(
            "Отправка запроса на создание билд конфигурации с пустым 'name' полем"
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
        'Отправка запроса на создание билд конфигурации с invalid data в поле "project_id" с разными ролями'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-15")
    @allure.title(
        'Проверка создания билд конфигурации с невалидными данными в поле "project_id"'
    )
    @allure.description(
        'Негативный тест создание билд конфигурации с невалидными данными в поле "project_id".'
    )
    def test_create_build_conf_with_invalid_project_id(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data_with_invalid_project_id,
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_model_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Проверка нахождения id созданного проекта в общем списке проектов"
        ):
            get_project_response = (
                super_admin.api_manager.project_api.get_project_by_locator(
                    project_data_1.id
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
        ):
            project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert (
                project_response.id == project_data_1.id
            ), f"There is no project with {project_data_1.id} id"
        with allure.step(
            "Отправка запроса на создание билд конфигурации с невалидными данными в 'project_id' поле"
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

    @allure.feature("Управление билд конфигурациями")
    @allure.story(
        'Отправка запроса на создание билд конфигурации с пустым полем "steps" с разными ролями'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-16")
    @allure.title('Проверка создания билд конфигурации с пустым полем "steps"')
    @allure.description(
        'Тест проверяет создание билд конфигурации с пустым полем "steps".'
    )
    def test_create_build_conf_with_empty_steps_field(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data_with_empty_steps_field,
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_model_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Проверка нахождения id созданного проекта в общем списке проектов"
        ):
            get_project_response = (
                super_admin.api_manager.project_api.get_project_by_locator(
                    project_data_1.id
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
        ):
            project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert project_response.id == project_data_1.id, (
                f"There is no project" f" with {project_data_1.id} id"
            )
        with allure.step(
            "Отправка запроса на создание билд конфигурации с пустым 'steps' полем"
        ):
            build_conf_data_1 = build_conf_data_with_empty_steps_field()
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданной билд конфигурации с отправленными данными"
        ):
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )

        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"

    @allure.feature("Управление билд конфигурациями")
    @allure.story(
        'Отправка запроса на создание билд конфигурации без поля "steps" с разными ролями'
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-17")
    @allure.title('Проверка создания билд конфигурации без поля "steps"')
    @allure.description('Тест проверяет создание билд конфигурации без поля "steps".')
    def test_create_build_conf_without_steps_field(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data_without_steps_field,
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
            )
        with allure.step(
            "Проверка нахождения id созданного проекта в общем списке проектов"
        ):
            get_project_response = (
                super_admin.api_manager.project_api.get_project_by_locator(
                    project_data_1.id
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
        ):
            project_response = ProjectResponseModel.model_validate_json(
                get_project_response
            )
        with pytest.assume:
            assert project_response.id == project_data_1.id, (
                f"There is no project with" f" {project_data_1.id} id"
            )
        with allure.step(
            "Отправка запроса на создание билд конфигурации без поля 'steps'"
        ):
            build_conf_data_1 = build_conf_data_without_steps_field()
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданной билд конфигурации с отправленными данными"
        ):
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"


class TestBuildConfCreateWithAlreadyUsedIdAndName:

    @allure.feature("Управление билд конфигурациями")
    @allure.story(
        "Отправка запроса на создание билд конфигурации с name, которое уже используется, с разными ролями"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-18")
    @allure.title(
        'Проверка создания билд конфигурации с уже существующим "name" билд конфигурации'
    )
    @allure.description(
        'Негативный тест проверяет создание билд конфигурации с уже существующим "name" билд конфигурации.'
    )
    def test_create_build_conf_when_build_conf_exists_with_name(
        self, super_admin, user_create, project_data, build_conf_data
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_model_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_model_response.parentProjectId}' given in response"
            )
        with allure.step("Отправка запроса на создание билд конфигурации"):
            build_conf_data_1 = build_conf_data
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданной билд конфигурации с отправленными данными"
        ):
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"
        with allure.step(
            "Отправка запроса на создание билд конфигурации с не уникальным 'name'"
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

    @allure.feature("Управление билд конфигурациями")
    @allure.story(
        "Отправка запроса на создание билд конфигурации с id, которое уже используется, с разными ролями"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/2", name="Тест-кейс-19")
    @allure.title(
        'Проверка создания билд конфигурации с уже существующим "id" билд конфигурации'
    )
    @allure.description(
        'Негативный тест проверяет создание билд конфигурации с уже существующим "id" билд конфигурации.'
    )
    def test_create_build_conf_when_build_conf_exists_with_id(
        self, super_admin, user_create, project_data, build_conf_data
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
            )
        with allure.step("Отправка запроса на создание билд конфигурации"):
            build_conf_data_1 = build_conf_data
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданной билд конфигурации с отправленными данными"
        ):
            build_response = BuildResponseModel.model_validate_json(
                build_config_response
            )
        with pytest.assume:
            assert (
                build_response.id == build_conf_data_1.id
            ), f"expected build conf id= {build_conf_data_1.id}, but '{build_response.id}' given"
        with allure.step(
            "Отправка запроса на создание билд конфигурации с неуникальным 'id'"
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

    @allure.feature("Управление билд конфигурациями")
    @allure.story(
        "Отправка запроса на копирование уже существующей билд конфигурации с разными ролями"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/2", name="Тест-кейс-20")
    @allure.title("Проверка копирования билд конфигурации")
    @allure.description(
        'Тест проверяет копирование билд конфигурации в текущий проект".'
    )
    def test_project_copy(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data,
        build_conf_data_copy,
    ):
        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
            )
        with allure.step("Отправка запроса на создание билд конфигурации"):
            build_conf_data_1 = build_conf_data
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданной билд конфигурации с отправленными данными"
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
            "Отправка запроса на создание копии уже существующей билд конфигурации"
        ):
            build_conf_data_copy_1 = build_conf_data_copy
            copy_build_conf_response = (
                super_admin.api_manager.build_conf_api.create_build_conf_copy(
                    build_conf_data_copy_1.model_dump(), project_data_1.id
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданной копии билд конфигурации с отправленными данными"
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
        "Отправка запроса на копирование уже существующей билд конфигурации с неизвестным source build conf с разными ролями"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/2", name="Тест-кейс-21")
    @allure.title(
        'Проверка копирования билд конфигурации с неизвестным "id" source build conf'
    )
    @allure.description(
        'Негативный тест проверяет создание  билд конфигурации путем копирования с использованием неизвестным "id" source build conf.'
    )
    def test_build_conf_copy_with_invalid_source_build_conf(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data,
        build_conf_data_copy_with_invalid_parent_build_conf,
    ):
        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
            )
        with allure.step("Отправка запроса на создание билд конфигурации"):
            build_conf_data_1 = build_conf_data
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданной билд конфигурации с отправленными данными"
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
            "Отправка запроса на создание копии уже существующей билд конфигурации с неизвестным source build conf"
        ):
            build_copy_1 = build_conf_data_copy_with_invalid_parent_build_conf
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

    @allure.feature("Управление билд конфигурациями")
    @allure.story(
        "Отправка запроса на создание, удаление билд конфигурации и получением информации о ней с разными ролями"
    )
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://example.com/docs/create_project", name="Документация")
    @allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
    @allure.testcase("https://testcase.manager/testcase/456", name="Тест-кейс-22")
    @allure.title(
        "Проверка создания, удаления билд конфигурации и получения информации о ней"
    )
    @allure.description(
        "Негативный тест проверяет создание билд конфигурации, ее удаление и запрос информации о ней."
    )
    def test_create_build_conf_delete_and_get_info(
        self,
        super_admin,
        user_create,
        project_data,
        build_conf_data_without_deleting_id,
    ):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = (
                super_admin.api_manager.project_api.create_project(
                    project_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданного проекта с отправленными данными"
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
                project_response.parentProjectId
                == project_data_1.parentProject["locator"]
            ), (
                f"expected parent project id= {project_data_1.parentProject['locator']},"
                f" but '{project_response.parentProjectId}' given in response"
            )
        with allure.step("Отправка запроса на создание билд конфигурации"):
            build_conf_data_1 = build_conf_data_without_deleting_id
            build_config_response = (
                super_admin.api_manager.build_conf_api.create_build_conf(
                    build_conf_data_1.model_dump()
                ).text
            )
        with allure.step(
            "Проверка соответствия параметров созданной билд конфигурации с отправленными данными"
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
            "Отправка запроса на получение информации об удаленной билд конфигурации"
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
