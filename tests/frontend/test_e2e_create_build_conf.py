import time
from http import HTTPStatus
import allure
import pytest
from data.build_conf_data import BuildResponseModel
from data.project_data import ProjectResponseModel
from pages.create_project_page import ProjectCreationPage, CreateTheFirstProjectPage
from pages.edit_build_conf_page import BuildConfCopyPage, BuildConfDeletePage, BuildConfCopyErrorPage
from pages.login_page import LoginPage, LoginPageFirstTime
from pages.edit_project_page import EditProjectFormPage
from pages.create_build_conf_page import BuildConfCreationPage, BuildConfCreationWithErrorPage
from resources.user_creds import UsualUserCreds
from utilis.data_generator import DataGenerator


@allure.feature('Управление билд конфигурациями')
@allure.story('Создание билд конфигурации с невалидными данными')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-204')
@allure.title('Проверка создания билд конфигурации с пустыми обязательными полями, невалидным id, с уже существующим именем билд конфигурации')
@allure.description('Негативный тест проверяет создание билд конфигурации с пустыми обязательными полями, невалидным id, с уже существующим именем билд конфигурации.')

def test_create_build_conf_with_invalid_data(browser, project_data, super_admin, build_conf_data):
    project_data_1 = project_data
    project_id = project_data_1.id
    project_name = project_data_1.name
    build_conf_data_1 = build_conf_data
    build_conf_id = build_conf_data_1.id
    build_conf_name = build_conf_data_1.name
    description = DataGenerator.random_text()
    invalid_build_id = DataGenerator.incorrect_id_1()
    project_parent = project_data_1.parentProject["locator"]


    with allure.step("Авторизация пользователя"):
        login_browser = LoginPageFirstTime(browser)
        login_browser.login_in_account(UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
    with allure.step("Создание первого проекта"):
        first_project_creation_browser = CreateTheFirstProjectPage(browser)
        first_project_creation_browser.create_first_project(project_name, project_id, description)
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.check_project_data(project_name, project_id, description)
        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            response = super_admin.api_manager.project_api.get_project_by_locator(project_data_1.id).text
            created_project = ProjectResponseModel.model_validate_json(response)
            with pytest.assume:
                assert created_project.id == project_id, \
                    f"expected project id = {project_id}, but '{created_project.id}' given"
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, \
                    f"expected parent project = {project_parent}, but '{created_project.parentProjectId}' given"
    with allure.step("Cоздание билд конфигурации"):
        build_conf_creation_browser = BuildConfCreationPage(browser, project_id)
        build_conf_creation_browser.create_build_conf(build_conf_id, build_conf_name, project_id, build_conf_name)
    with allure.step("Проверка нахождения id созданной билд конфигурации в общем списке билд конфигураций"):
        get_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(build_conf_data_1.id).text
    with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
        build_conf_model_response_1 = BuildResponseModel.model_validate_json(get_build_conf_response)
        assert build_conf_model_response_1.id == build_conf_data_1.id, \
            f"expected build conf id= {build_conf_data_1.id}, but '{build_conf_model_response_1.id}' given"
    with allure.step("Создание билд конфигурации с пустыми полями имени и id"):
        build_conf_error = BuildConfCreationWithErrorPage(browser, project_id)
        build_conf_error.create_build_conf_with_empty_fields(" ", " ", description)
    with allure.step("Создание билд конфигурации с невалидным id"):
        build_conf_error.create_build_conf_with_invalid_build_id(invalid_build_id, build_conf_name, str(invalid_build_id[0]), description)
    with allure.step("Создание билд конфигурации с уже существующим именем билда"):
        build_conf_error.create_build_conf_with_used_build_name(project_id, build_conf_name, project_name, description)
    with allure.step("Отправка запроса на получение информации билд конфигурации, которую попробовали создать"):
        get_about_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(project_id, expected_status=HTTPStatus.NOT_FOUND)
    with pytest.assume:
        assert f"NotFoundException: No build type nor template is found by id '{project_id}'" in get_about_build_conf_response.text


@allure.feature('Управление билд конфигурациями')
@allure.story('Создание копии билд конфигурации')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-205')
@allure.title('Проверка создания копии билд конфигурации с изменением id билд конфигурации')
@allure.description('Позитивный тест проверяет создания копии билд конфигурации с изменением id билд конфигурации.')

def test_create_build_conf_by_copy(browser, project_data, super_admin, build_conf_data, project_data_first_project):
    project_data_1 = project_data
    project_id = project_data_1.id
    project_name = project_data_1.name
    build_conf_data_1 = build_conf_data
    build_conf_id = build_conf_data_1.id
    build_conf_name = build_conf_data_1.name
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]
    new_build_conf_id = DataGenerator.fake_project_id()


    with allure.step("Отправка запроса на создание первого проекта"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(project_data_2.model_dump()).text
    with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
        project_model_response = ProjectResponseModel.model_validate_json(create_project_response)
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, \
            f"expected project id= {project_data_2.id}, but '{project_model_response.id}' given"
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
    with allure.step("Создание проекта"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(project_name, project_id, description)
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.check_project_data(project_name, project_id, description)
        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            response = super_admin.api_manager.project_api.get_project_by_locator(project_data_1.id).text
            created_project = ProjectResponseModel.model_validate_json(response)
            with pytest.assume:
                assert created_project.id == project_id, \
                    f"expected project id = {project_id}, but '{created_project.id}' given"
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, \
                    f"expected parent project = {project_parent}, but '{created_project.parentProjectId}' given"
    with allure.step("Cоздание билд конфигурации"):
        build_conf_creation_browser = BuildConfCreationPage(browser, project_id)
        build_conf_creation_browser.create_build_conf(build_conf_id, build_conf_name, project_id, description)
    with allure.step("Проверка отображения версии билда приложения"):
        build_conf_creation_browser.footer.check_build_version_is_visible()
    with allure.step("Проверка отображения имени приложения"):
        build_conf_creation_browser.footer.check_app_name_is_visible()
    with allure.step("Проверка отображения текста копирайтинга"):
        build_conf_creation_browser.footer.check_copyright_text_is_visible()
    with allure.step("Проверка нахождения id созданной билд конфигурации в общем списке билд конфигураций"):
        get_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(build_conf_data_1.id).text
    with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
        build_conf_model_response_1 = BuildResponseModel.model_validate_json(get_build_conf_response)
        assert build_conf_model_response_1.id == build_conf_data_1.id, \
            f"expected build conf id= {build_conf_data_1.id}, but '{build_conf_model_response_1.id}' given"
    with allure.step("Копирование билд конфигурации"):
        copy_build_conf = BuildConfCopyPage(browser, build_conf_id)
        copy_build_conf.copy_build_conf(new_build_conf_id, new_build_conf_id)
    with allure.step("Удаление билд конфигурации"):
        build_conf_delete = BuildConfDeletePage(browser, new_build_conf_id)
        build_conf_delete.delete_build_conf(project_id, new_build_conf_id)
    with allure.step("Отправка запроса на получение информации об удаленной билд конфигурации"):
        get_about_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(new_build_conf_id, expected_status=HTTPStatus.NOT_FOUND)
    with pytest.assume:
        assert f"NotFoundException: No build type nor template is found by id '{new_build_conf_id}'" in get_about_build_conf_response.text



@allure.feature('Управление билд конфигурациями')
@allure.story('Создание копии билд конфигурации с невалидными данными')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-206')
@allure.title('Проверка создания копии билд конфигурации с невалидным id')
@allure.description('Негативный тест проверяет создания копии билд конфигурации с невалидным id .')

def test_create_invalid_copy_build_conf(browser, project_data, super_admin, build_conf_data_without_deleting_id, project_data_first_project):
    project_data_1 = project_data
    project_id = project_data_1.id
    project_name = project_data_1.name
    build_conf_data_1 = build_conf_data_without_deleting_id
    build_conf_id = build_conf_data_1.id
    build_conf_name = build_conf_data_1.name
    description = DataGenerator.random_text()
    invalid_build_id = DataGenerator.incorrect_id_1()
    project_parent = project_data_1.parentProject["locator"]


    with allure.step("Отправка запроса на создание первого проекта"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(project_data_2.model_dump()).text
    with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
        project_model_response = ProjectResponseModel.model_validate_json(create_project_response)
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, \
            f"expected project id= {project_data_2.id}, but '{project_model_response.id}' given"
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
    with allure.step("Создание проекта"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(project_name, project_id, description)
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.check_project_data(project_name, project_id, description)
        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            response = super_admin.api_manager.project_api.get_project_by_locator(project_data_1.id).text
            created_project = ProjectResponseModel.model_validate_json(response)
            with pytest.assume:
                assert created_project.id == project_id, \
                    f"expected project id = {project_id}, but '{created_project.id}' given"
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, \
                    f"expected parent project = {project_parent}, but '{created_project.parentProjectId}' given"
    with allure.step("Cоздание билд конфигурации"):
        build_conf_creation_browser = BuildConfCreationPage(browser, project_id)
        build_conf_creation_browser.create_build_conf(build_conf_id, build_conf_name, project_id, build_conf_name)
    with allure.step("Проверка нахождения id созданной билд конфигурации в общем списке билд конфигураций"):
        get_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(build_conf_data_1.id).text
    with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
        build_conf_model_response_1 = BuildResponseModel.model_validate_json(get_build_conf_response)
        assert build_conf_model_response_1.id == build_conf_data_1.id, \
            f"expected build conf id= {build_conf_data_1.id}, but '{build_conf_model_response_1.id}' given"
    with allure.step("Копирование билд конфигурации с невалидным id"):
        copy_build_conf = BuildConfCopyErrorPage(browser, build_conf_id)
        copy_build_conf.copy_build_conf_error(invalid_build_id, invalid_build_id, str(invalid_build_id[0]), build_conf_name)
    with allure.step("Удаление билд конфигурации"):
        build_conf_delete = BuildConfDeletePage(browser, build_conf_name)
        build_conf_delete.delete_build_conf(project_id, build_conf_name)
    with allure.step("Отправка запроса на получение информации об удаленной билд конфигурации"):
        get_about_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(project_id, expected_status=HTTPStatus.NOT_FOUND)
    with pytest.assume:
        assert f"NotFoundException: No build type nor template is found by id '{project_id}'" in get_about_build_conf_response.text