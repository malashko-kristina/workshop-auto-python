import copy
from http import HTTPStatus
import pytest
import allure
from data.project_data import ProjectResponseModel
from utilis.data_generator import DataGenerator


class TestProjectCreateWithInvalidData:

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на создание проекта с пустым полем "id" с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-1')
    @allure.title('Проверка создания проекта с пустым полем "id"')
    @allure.description('Негативный тест проверяет создание нового проекта с пустым полем "id".')
    def test_create_project_with_empty_id(self, super_admin, user_create, project_data_with_empty_id):
        with allure.step("Отправка запроса на создание проекта c пустым id"):
            invalid_project_data = project_data_with_empty_id()
            create_project_response = super_admin.api_manager.project_api.create_project(
                invalid_project_data.model_dump(), expected_status=HTTPStatus.INTERNAL_SERVER_ERROR)

        with pytest.assume:
            assert "InvalidIdentifierException: Project ID must not be empty" in create_project_response.text

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на создание проекта с невалидными данными в поле "id" с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/2', name='Тест-кейс-2')
    @allure.title('Проверка создания проекта с невалидными данными в поле "id"')
    @allure.description('Негативный тест проверяет создание нового проекта с невалидными данными в поле "id".')
    def test_create_project_with_invalid_ids(self, super_admin, user_create, project_data_with_invalid_ids):

        with allure.step("Отправка запроса на создание проекта c невалидными полем 'id'"):
            invalid_project_data = project_data_with_invalid_ids
            create_project_response = super_admin.api_manager.project_api.create_project(
                invalid_project_data.model_dump(), expected_status=HTTPStatus.INTERNAL_SERVER_ERROR)

        with pytest.assume:
            assert "ID should start with a latin letter and contain only latin letters, digits and underscores (at most 225 characters)" in create_project_response.text

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на создание проекта с пустым полем "name" с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-3')
    @allure.title('Проверка создания проекта с пустым полем "name"')
    @allure.description('Негативный тест проверяет создание нового проекта с пустым полем "name".')
    def test_create_project_with_empty_name(self, super_admin, user_create, project_data_with_invalid_name):

        with allure.step("Отправка запроса на создание проекта c пустым полем 'name''"):
            invalid_project_data = project_data_with_invalid_name()
            create_project_response = super_admin.api_manager.project_api.create_project(
                invalid_project_data.model_dump(), expected_status=HTTPStatus.BAD_REQUEST)

        with pytest.assume:
            assert "BadRequestException: Project name cannot be empty" in create_project_response.text

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на создание проекта с пустым полем "parentProject" с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-4')
    @allure.title('Проверка создания проекта с пустым полем "parentProject"')
    @allure.description('Негативный тест проверяет создание нового проекта с пустым полем "parentProject".')
    def test_create_project_with_empty_parentProject(self, super_admin, user_create, project_data_with_empty_parentProject):

        with allure.step("Отправка запроса на создание проекта c пустым полем 'parentProject'"):
            invalid_project_data = project_data_with_empty_parentProject()
            create_project_response = super_admin.api_manager.project_api.create_project(
                invalid_project_data.model_dump(), expected_status=HTTPStatus.BAD_REQUEST)

        with pytest.assume:
            assert "BadRequestException: No project specified. Either 'id', 'internalId' or 'locator' attribute should be present" in create_project_response.text

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на создание проекта с невалидными данными в поле "parentProject" с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/2', name='Тест-кейс-5')
    @allure.title('Проверка создания проекта с невалидными данными в поле "parentProject"')
    @allure.description('Негативный тест проверяет создание нового проекта с невалидными данными в поле "parentProject".')
    def test_create_project_with_invalid_parentProject(self, super_admin, user_create, project_data_with_invalid_parentProject):

        with allure.step("Отправка запроса на создание проекта c невалидными данными в поле 'parentProject'"):
            invalid_project_data = project_data_with_invalid_parentProject
            create_project_response = super_admin.api_manager.project_api.create_project(
                invalid_project_data.model_dump(), expected_status=HTTPStatus.NOT_FOUND)

        with pytest.assume:
            assert f"NotFoundException: No project found by name or internal/external id" in create_project_response.text


class TestProjectCreateWithVariantData:

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на создание проекта с булевым значением "False" в "copyAllAssociatedSettings" с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/2', name='Тест-кейс-6')
    @allure.title('Проверка создания проекта с булевым значением "False" в "copyAllAssociatedSettings"')
    @allure.description('Тест проверяет создание нового проекта с булевым значением "False" в "copyAllAssociatedSettings".')
    def test_create_project_with_false(self, super_admin, user_create, project_data_with_false):

        with allure.step("Отправка запроса на создание проекта с булевым значением false в поле 'copyAllAssociatedSettings'"):
            project_data_2 = project_data_with_false()
            create_project_response = super_admin.api_manager.project_api.create_project(
                project_data_2.model_dump()).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response)

        with pytest.assume:
            assert project_model_response.id == project_data_2.id, \
                f"expected project id= {project_data_2.id}, but '{project_model_response.id}' given"

        with pytest.assume:
            assert project_model_response.parentProjectId == project_data_2.parentProject["locator"], \
                (f"expected parent project id= {project_data_2.parentProject['locator']},"
                 f" but '{project_model_response.parentProjectId}' given in response")


class TestProjectCreateWithTheSameData:

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на создание проекта с уже существующим "name" другого проекта с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/2', name='Тест-кейс-7')
    @allure.title('Проверка создания проекта с уже существующим "name" другого проекта')
    @allure.description('Негативный тест проверяет создание нового проекта с уже существующим "name" другого проекта".')
    def test_create_project_when_project_exists_with_name(self, super_admin, user_create, project_data):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response)
        with pytest.assume:
            assert project_model_response.id == project_data_1.id, \
                f"expected project id= {project_data_1.id}, but '{
                    project_model_response.id}' given"
        with allure.step("Отправка запроса на создание проекта с таким же именем, которое использовалось в прошлом запросе"):
            create_project_response_2 = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump(), expected_status=HTTPStatus.BAD_REQUEST)
        with pytest.assume:
            assert "DuplicateProjectNameException: Project with this name already exists" in create_project_response_2.text

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на создание проекта с уже существующим "id" другого проекта с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/2', name='Тест-кейс-8')
    @allure.title('Проверка создания проекта с уже существующим "id" другого проекта')
    @allure.description('Негативный тест проверяет создание нового проекта с уже существующим "id" другого проекта".')
    def test_create_project_when_project_exists_with_id(self, super_admin, user_create, project_data):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data
            create_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response)
        with pytest.assume:
            assert project_model_response.id == project_data_1.id, \
                f"expected project id= {project_data_1.id}, but '{
                    project_model_response.id}' given"
        with allure.step("Отправка запроса на создание проекта с таким же id, которое использовалось в прошлом запросе"):
            project_data_2 = copy.deepcopy(project_data_1)
            project_data_2.name = DataGenerator.fake_build_id()
            create_project_response_2 = super_admin.api_manager.project_api.create_project(
                project_data_2.model_dump(), expected_status=HTTPStatus.BAD_REQUEST)
        with pytest.assume:
            assert f'DuplicateExternalIdException: Project ID "{
                project_data_1.id}" is already used by another project' in create_project_response_2.text


class TestProjectCopy:

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на копирование существующего проекта с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/2', name='Тест-кейс-9')
    @allure.title('Проверка копирования проекта с уже существующего проекта')
    @allure.description('Тест проверяет создание нового проекта на основе уже существующего проекта путем копирования".')
    def test_project_copy(self, super_admin, user_create, project_data, project_copy_data):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_3 = project_data
            create_project_response = super_admin.api_manager.project_api.create_project(
                project_data_3.model_dump()).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response)
        with pytest.assume:
            assert project_model_response.id == project_data_3.id, \
                f"expected project id= {project_data_3.id}, but '{
                    project_model_response.id}' given"
        with pytest.assume:
            assert project_model_response.parentProjectId == project_data_3.parentProject["locator"], \
                (f"expected parent project id= {project_data_3.parentProject['locator']},"
                 f" but '{project_model_response.parentProjectId}' given in response")
        with allure.step("Отправка запроса на создание копии уже существующего проекта"):
            project_copy_data_1 = project_copy_data
            create_project_copy_response = super_admin.api_manager.project_api.create_copy_project(
                project_copy_data_1.model_dump()).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            project_copy_model_response = ProjectResponseModel.model_validate_json(
                create_project_copy_response)
        with pytest.assume:
            assert project_copy_model_response.id == project_copy_data_1.id, \
                f"expected project id= {project_copy_data_1.id}, but '{
                    project_copy_model_response.id}' given"
        with pytest.assume:
            assert project_copy_model_response.parentProjectId == project_copy_data_1.parentProject["locator"], \
                (f"expected parent project id= {
                 project_copy_data_1.parentProject['locator']},")

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на копирование проекта с неизвестным id проекта с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/2', name='Тест-кейс-10')
    @allure.title('Проверка копирования проекта с неизвестным id проекта')
    @allure.description('Негативный тест проверяет создание нового проекта путем копирования с использованием несуществуюшего id проекта".')
    def test_project_copy_with_invalid_source_project(self, super_admin, user_create, project_data, project_copy_data_with_another_source_project):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_3 = project_data
            create_project_response = super_admin.api_manager.project_api.create_project(
                project_data_3.model_dump()).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response)
        with pytest.assume:
            assert project_model_response.id == project_data_3.id, \
                f"expected project id= {project_data_3.id}, but '{
                    project_model_response.id}' given"
        with pytest.assume:
            assert project_model_response.parentProjectId == project_data_3.parentProject["locator"], \
                (f"expected parent project id= {project_data_3.parentProject['locator']},"
                 f" but '{project_model_response.parentProjectId}' given in response")
        with allure.step("Отправка запроса на создание копии уже существующего проекта, но с указанием неизвестного id"):
            project_copy_data_2 = project_copy_data_with_another_source_project()
            create_project_copy_response = super_admin.api_manager.project_api.create_copy_project(
                project_copy_data_2.model_dump(), expected_status=HTTPStatus.NOT_FOUND)
        with pytest.assume:
            assert f"NotFoundException: No project found by name or internal/external id '{
                project_copy_data_2.sourceProject['locator']}'" in create_project_copy_response.text


class TestProjectCreateAndDelete:

    @allure.feature('Управление проектами')
    @allure.story('Отправка запроса на получение информации об удаленном проекте с разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/2', name='Тест-кейс-11')
    @allure.title('Проверка запроса на получение информации об удаленном проекте')
    @allure.description('Тест проверяет создание нового проекта, его удаление и получение информации об удаленном проекте".')
    def test_create_project_and_delete(self, super_admin, user_create, project_data_without_deleting):

        with allure.step("Отправка запроса на создание проекта"):
            project_data_1 = project_data_without_deleting()
            create_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response)
        with pytest.assume:
            assert project_model_response.id == project_data_1.id, \
                f"expected project id= {project_data_1.id}, but '{
                    project_model_response.id}' given"
        with allure.step("Отправка запроса на удаление созданного проекта"):
            delete_project_response = super_admin.api_manager.project_api.delete_project(
                project_model_response.id)
        with pytest.assume:
            assert delete_project_response.status_code == 204
        with allure.step("Отправка запроса на получение информации об удаленно проекте"):
            get_delete_project_response = super_admin.api_manager.project_api.get_project_by_locator(
                project_model_response.id, expected_status=HTTPStatus.NOT_FOUND)
        with pytest.assume:
            assert f"NotFoundException: No project found by name or internal/external id '{
                project_data_1.id}'" in get_delete_project_response.text
