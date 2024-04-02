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


@allure.feature('Управление проектами')
@allure.story('Создание первого проекта')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-199')
@allure.title('Проверка создания первого проекта')
@allure.description('Позитивный тест проверяет создание первого проекта в аккаунте.')
def test_create_the_first_project(browser, project_data_create, super_admin, project_data_without_deleting, delete_all_projects):
    project_data_1 = project_data_create()
    project_id = project_data_1.id
    project_name = project_data_1.name
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
        login_browser.check_url_favourite_projects()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Создание первого проекта"):
        go_to_first_project_creation_browser = CreateTheFirstProjectPage(
            browser)
        go_to_first_project_creation_browser.tap_on_create_first_project()
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.create_project_manually(
            project_name, project_id, description)
        project_creation_browser.check_url_after_project_creation(project_id)
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description)
    with allure.step('Отправка запроса на получение информации о созданном проекте'):
        response = super_admin.api_manager.project_api.get_project_by_locator(
            project_name).text
        created_project = ProjectResponseModel.model_validate_json(response)
        with pytest.assume:
            assert created_project.id == project_id, \
                f"expected project id = {project_id}, but '{created_project.id}' given"
        with pytest.assume:
            assert created_project.parentProjectId == project_parent, \
                (f"expected parent project = {project_parent},"
                 f" but '{created_project.parentProjectId}' given")
    with allure.step("Проверка отображения имени приложения"):
        edit_project_browser.footer.check_app_name_is_visible()
    with allure.step("Проверка отображения текста копирайтинга"):
        edit_project_browser.footer.check_copyright_text_is_visible()
    with allure.step("Выход из аккаунта"):
        edit_project_browser.header.go_to_logout_admin_panel_through_header_button()
    with allure.step("Проверка нахождения id созданного проекта в общем списке проектов"):
        get_project_response = super_admin.api_manager.project_api.get_project_by_locator(
            project_data_1.id).text
    with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
        created_model_project_response = ProjectResponseModel.model_validate_json(
            get_project_response)
        assert created_model_project_response.id == project_data_1.id, (f"There is no project with"
                                                                        f" {project_data_1.id} id")


@allure.feature('Управление проектами')
@allure.story('Создание проекта с пустым полем "id", с уже используемым id')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-200')
@allure.title('Проверка создания проекта с пустым полем "id", с уже используемым id')
@allure.description('Флоу негативных тестов проверяет создание нового проекта с пустым полем "id", с уже используемым id.')
def test_create_project_invalid_id_name(browser, project_data_create, super_admin, project_data_first_project):
    project_data_1 = project_data_create()
    project_id = project_data_1.id
    project_name = project_data_1.name
    project_name_2 = DataGenerator.fake_build_id()
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Отправка запроса на создание первого проекта"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()).text
    with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
        project_model_response = ProjectResponseModel.model_validate_json(
            create_project_response)
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, \
            f"expected project id= {project_data_2.id}, but '{
                project_model_response.id}' given"
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Переход на страницу создания проекта через хедер"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.header.go_to_create_projects_through_header_button()
    with allure.step("Создание проекта через хедер"):
        project_creation_browser.create_project_manually(
            project_name, project_id, description)
        project_creation_browser.check_url_after_project_creation(project_id)
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description)
    with allure.step('Отправка запроса на получение информации о созданном проекте'):
        response = super_admin.api_manager.project_api.get_project_by_locator(
            project_name).text
        created_project = ProjectResponseModel.model_validate_json(response)
        with pytest.assume:
            assert created_project.id == project_id, \
                f"expected project id = {project_id}, but '{created_project.id}' given"
        with pytest.assume:
            assert created_project.parentProjectId == project_parent, \
                f"expected parent project = {project_parent}, but '{
                    created_project.parentProjectId}' given"
    with allure.step("Создание проекта с пустым именем"):
        project_creation_with_error_browser = ProjectCreationPage(browser)
        project_creation_with_error_browser.go_to_creation_page()
        project_creation_with_error_browser.create_project_manually(
            "", project_id, description)
        project_creation_with_error_browser.check_error_empty_project_name_is_visible()
    with allure.step("Создание проекта с уже используемым id"):
        project_creation_with_error_browser.create_project_manually(
            project_name_2, project_id, description)
        project_creation_with_error_browser.check_error_invalid_project_id_is_visible(
            project_id)
    with allure.step("Проверка отображения версии билда приложения"):
        project_creation_with_error_browser.footer.check_build_version_is_visible()
    with allure.step("Проверка отображения имени приложения"):
        project_creation_with_error_browser.footer.check_app_name_is_visible()
    with allure.step("Проверка отображения текста копирайтинга"):
        project_creation_with_error_browser.footer.check_copyright_text_is_visible()


@allure.feature('Управление проектами')
@allure.story('Изменение данных проекта с использованием невалидного id с последующим корректным его изменением')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-201')
@allure.title('Изменение данных проекта с использованием невалидного id с последующим корректным его изменением')
@allure.description('Флоу из негативный теста по изменению проекта с невалидным id с последующим корректным его изменением.')
def test_create_project_invalid_id_edit(browser, project_data_without_deleting, super_admin, project_data_first_project):
    project_data_1 = project_data_without_deleting()
    project_id = project_data_1.id
    project_name = project_data_1.name
    project_id_invalid = DataGenerator.incorrect_id_1()
    project_id_2 = DataGenerator.fake_build_id()
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Отправка запроса на создание первого проекта"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()).text
    with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
        project_model_response = ProjectResponseModel.model_validate_json(
            create_project_response)
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, \
            f"expected project id= {project_data_2.id}, but '{
                project_model_response.id}' given"
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Создание проекта"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(
            project_name, project_id, description)
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description)
        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_name).text
            created_project = ProjectResponseModel.model_validate_json(
                response)
            with pytest.assume:
                assert created_project.id == project_id, \
                    f"expected project id = {project_id}, but '{
                        created_project.id}' given"
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, \
                    f"expected parent project = {project_parent}, but '{
                        created_project.parentProjectId}' given"
    with allure.step("Редактирование проекта с использованием невалидного id"):
        project_invalid_edit_browser = EditProjectFormPage(browser, project_id)
        project_invalid_edit_browser.check_project_url_edit()
        project_invalid_edit_browser.add_changes_to_project_data(
            project_name, project_id_invalid, description)
        project_invalid_edit_browser.check_warning_message_edit()
        project_invalid_edit_browser.tap_on_save_changes_button()
        project_invalid_edit_browser.check_error_message_invalid_project_id_edit(
            project_id_invalid)
    with allure.step("Редактирование проекта с использованием валидных данных"):
        project_edit_browser = EditProjectFormPage(browser, project_id)
        project_edit_browser.check_project_url_edit()
        project_edit_browser.add_changes_to_project_data(
            project_name,  project_id_2, description)
        project_edit_browser.tap_on_save_changes_button()
        project_edit_browser.check_success_message_edit_saved()
    with allure.step("Удаление проекта"):
        delete_project_browser = EditProjectFormPage(browser, project_id_2)
        delete_project_browser.check_project_url_edit()
        delete_project_browser.delete_project()
    with allure.step("Отправка запроса на получение информации об удаленно проекте"):
        get_delete_project_response = super_admin.api_manager.project_api.get_project_by_locator(
            project_id_2, expected_status=HTTPStatus.NOT_FOUND)
    with pytest.assume:
        assert f"NotFoundException: No project found by name or internal/external id '{
            project_id_2}'" in get_delete_project_response.text


@allure.feature('Управление проектами')
@allure.story('Создание копии уже существующего проекта с изменением id')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-202')
@allure.title('Проверка создания копии проекта')
@allure.description('Позитивный тест проверяет создание нового проекта на основе копирования с уже существующего.')
def test_create_project_by_copy(browser, project_data_create, super_admin, project_data_first_project):
    project_data_1 = project_data_create()
    project_id = project_data_1.id
    project_name = project_data_1.name
    description = DataGenerator.random_text()
    project_id_new = DataGenerator.fake_build_id()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Отправка запроса на создание первого проекта"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()).text
    with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
        project_model_response = ProjectResponseModel.model_validate_json(
            create_project_response)
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, \
            f"expected project id= {project_data_2.id}, but '{
                project_model_response.id}' given"
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Создание проекта"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(
            project_name, project_id, description)
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description)
        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_name).text
            created_project = ProjectResponseModel.model_validate_json(
                response)
            with pytest.assume:
                assert created_project.id == project_id, \
                    f"expected project id = {project_id}, but '{
                        created_project.id}' given"
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, \
                    f"expected parent project = {project_parent}, but '{
                        created_project.parentProjectId}' given"
    with allure.step("Создание копии проекта"):
        edit_project_browser.check_project_url_edit()
        edit_project_browser.copy_project(project_id_new)
        edit_project_browser.check_success_message_project_copy()
    with allure.step("Проверка нахождения id созданного проекта в общем списке проектов"):
        get_project_response = super_admin.api_manager.project_api.get_project_by_locator(
            project_id_new).text
    with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
        created_model_project_response = ProjectResponseModel.model_validate_json(
            get_project_response)
    with pytest.assume:
        assert created_model_project_response.id == project_id_new, f"There is no project with {
            project_id_new} id"
    with allure.step("Удаление проекта"):
        delete_project_browser = EditProjectFormPage(browser, project_id_new)
        delete_project_browser.check_project_url_edit()
        delete_project_browser.delete_project()
    with allure.step("Отправка запроса на получение информации об удаленно проекте"):
        get_delete_project_response = super_admin.api_manager.project_api.get_project_by_locator(
            project_id_new, expected_status=HTTPStatus.NOT_FOUND)
    with pytest.assume:
        assert f"NotFoundException: No project found by name or internal/external id '{
            project_id_new}'" in get_delete_project_response.text


@allure.feature('Управление проектами')
@allure.story('Создание копии уже существующего проекта с пустым id')
@allure.severity(allure.severity_level.CRITICAL)
@allure.link('https://example.com/docs/create_project', name='Документация')
@allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
@allure.testcase('https://testcase.manager/testcase/1', name='Тест-кейс-203')
@allure.title('Проверка создания копии проекта с пустым полем "id"')
@allure.description('Негативный тест проверяет создание копии нового проекта с пустым полем "id".')
def test_create_project_by_copy_empty_id(browser, project_data_create, super_admin, project_data_first_project):
    project_data_1 = project_data_create()
    project_id = project_data_1.id
    project_name = project_data_1.name
    description = DataGenerator.random_text()
    project_id_empty = " "
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Отправка запроса на создание первого проекта"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()).text
    with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
        project_model_response = ProjectResponseModel.model_validate_json(
            create_project_response)
    with pytest.assume:
        assert project_model_response.id == project_data_2.id, \
            f"expected project id= {project_data_2.id}, but '{
                project_model_response.id}' given"
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD)
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Создание проекта"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(
            project_name, project_id, description)
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description)
        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            response = super_admin.api_manager.project_api.get_project_by_locator(
                project_name).text
            created_project = ProjectResponseModel.model_validate_json(
                response)
            with pytest.assume:
                assert created_project.id == project_id, \
                    f"expected project id = {project_id}, but '{
                        created_project.id}' given"
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, \
                    f"expected parent project = {project_parent}, but '{
                        created_project.parentProjectId}' given"
    with allure.step("Попытка создания копии проекта с пустым project id"):
        edit_project_browser.check_project_url_edit()
        edit_project_browser.copy_project(project_id_empty)
        edit_project_browser.check_error_message_project_copy()
    with allure.step("Отправка запроса на получение информации о несозданном проекте"):
        get_delete_project_response = super_admin.api_manager.project_api.get_project_by_locator(
            project_id_empty, expected_status=HTTPStatus.NOT_FOUND)
    with pytest.assume:
        assert f"NotFoundException: No project found by name or internal/external id '{
            project_id_empty}'" in get_delete_project_response.text
