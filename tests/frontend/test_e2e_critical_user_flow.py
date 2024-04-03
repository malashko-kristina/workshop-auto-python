import allure
import pytest
from data.build_conf_data import BuildResponseModel
from data.project_data import ProjectResponseModel
from data.run_build_data import BuildConfRunStatusModel
from pages.build_add_steps_page import BuildNewStepPage
from pages.buld_steps_page import BuildStepsPage
from pages.create_project_page import ProjectCreationPage
from pages.login_page import LoginPage
from pages.edit_project_page import EditProjectFormPage
from pages.create_build_conf_page import BuildConfCreationPage
from pages.run_build_conf_page import BuildConfRunPage
from pages.run_build_conf_with_step_page import RunBuildWithStep
from pages.vcs_root_page import AddVCSFormPage
from resources.user_creds import UsualUserCreds
from utilis.data_generator import DataGenerator


@allure.feature("Критический юзер флоу от создания проекта до запуска билда")
@allure.story("Создание проекта, билд конфигурации с последующим запуском")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://example.com/docs/create_project", name="Документация")
@allure.issue("https://issue.tracker/project/123", name="Баг-трекер")
@allure.testcase("https://testcase.manager/testcase/1", name="Тест-кейс-207")
@allure.title("Проверка создания проекта, билд конфигурации с последующим запуском")
@allure.description(
    "Позитивный тест проверяет критический юзер флоу от создания проекта до запуска билда."
)
def test_critical_user_flow(
    browser, project_data, super_admin, build_conf_data, project_data_first_project
):
    project_data_1 = project_data
    project_id = project_data_1.id
    project_name = project_data_1.name
    build_conf_data_1 = build_conf_data
    build_conf_id = build_conf_data_1.id
    build_conf_name = build_conf_data_1.name
    step_name = DataGenerator.fake_name()
    step_id = DataGenerator.fake_build_id()
    description = DataGenerator.random_text()
    project_parent = project_data_1.parentProject["locator"]

    with allure.step("Отправка запроса на создание первого проекта"):
        project_data_2 = project_data_first_project()
        create_project_response = super_admin.api_manager.project_api.create_project(
            project_data_2.model_dump()
        ).text
    with allure.step(
        "Проверка соответствия параметров созданного проекта с отправленными данными"
    ):
        project_model_response = ProjectResponseModel.model_validate_json(
            create_project_response
        )
    with pytest.assume:
        assert (
            project_model_response.id == project_data_2.id
        ), f"expected project id= {project_data_2.id}, but '{project_model_response.id}' given"
    with allure.step("Авторизация пользователя"):
        login_browser = LoginPage(browser)
        login_browser.login_in_account(
            UsualUserCreds.USER_LOGIN, UsualUserCreds.USER_PASSWORD
        )
        login_browser.check_url_favourite_projects_mode()
        login_browser.login_form_body.userpic_is_visible()
    with allure.step("Создание проекта"):
        project_creation_browser = ProjectCreationPage(browser)
        project_creation_browser.go_to_creation_page()
        project_creation_browser.create_project_manually(
            project_name, project_id, description
        )
    with allure.step("Проверка редиректа на страницу редактирования проекта"):
        edit_project_browser = EditProjectFormPage(browser, project_id)
        edit_project_browser.wait_edit_project_url()
        edit_project_browser.check_success_project_creation(
            project_name, project_id, description
        )
    with allure.step("Переход на страницу создания билд конфигурации"):
        edit_project_browser.redirect_to_create_build_conf(project_id)
        with allure.step(
            "Отправка запроса на получение информации о созданном проекте"
        ):
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
    with allure.step("Cоздание билд конфигурации"):
        build_conf_creation_browser = BuildConfCreationPage(browser, project_id)
        build_conf_creation_browser.create_build_conf(
            build_conf_id, build_conf_name, description
        )
        build_conf_creation_browser.check_url_after_build_create(
            build_conf_id, project_id
        )
    with allure.step(
        "Проверка нахождения id созданной билд конфигурации в общем списке билд конфигураций"
    ):
        get_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(
            build_conf_data_1.id
        ).text
    with allure.step(
        "Проверка соответствия параметров созданной билд конфигурации с отправленными данными"
    ):
        build_conf_model_response_1 = BuildResponseModel.model_validate_json(
            get_build_conf_response
        )
        assert build_conf_model_response_1.id == build_conf_data_1.id, (
            f"expected build conf id= {build_conf_data_1.id},"
            f" but '{build_conf_model_response_1.id}' given"
        )
    with allure.step("Проверка количества активных агентов"):
        response_2 = (
            super_admin.api_manager.agent_api.check_amount_of_authorized_agents()
        )
        count = str(response_2.json()["count"])
        project_creation_browser.header.check_agents_count_through_header_button(count)
    with allure.step(
        "Проверка успешности создания билд конфигурации и пропуск создания vcs"
    ):
        skip_vcs_browser = AddVCSFormPage(browser, build_conf_id, project_id)
        skip_vcs_browser.skip_vcs(build_conf_id, project_id)
    with allure.step("Запуск билд конфигурации без добавления шагов"):
        run_build_conf_without_steps = BuildConfRunPage(
            browser, project_id, build_conf_id
        )
        run_build_conf_without_steps.run_build_conf_ui()
    with allure.step(
        "Отправка запроса на проверку количества билд конфигураций в очереди для запуска"
    ):
        get_build_conf_run_response = (
            super_admin.api_manager.build_conf_api.check_query_with_build_conf().text
        )
    with allure.step(
        "Проверка соответствия параметров модели ответа запуска билд конфигурации с отправленными данными"
    ):
        build_run_response = BuildConfRunStatusModel.model_validate_json(
            get_build_conf_run_response
        )
        assert build_run_response.count == 0, (
            f"build was expected to be out of the query=0, but it is still here:"
            f" query={build_run_response.count}"
        )
    with allure.step(
        "Переход на страницу c кнопкой добавления шагов для билд конфигурации"
    ):
        go_to_build_steps_browser = BuildConfRunPage(browser, project_id, build_conf_id)
        go_to_build_steps_browser.tap_on_add_build_steps()
        go_to_add_build_steps = BuildStepsPage(browser, build_conf_id)
        go_to_add_build_steps.add_build_steps(build_conf_id)
    with allure.step("Проверка добавления шагов для билд конфигурации"):
        add_new_step_browser = BuildNewStepPage(browser, build_conf_id)
        add_new_step_browser.select_command_line()
        add_new_step_browser.add_new_build_step(
            step_name, step_id, "print('Hello World')"
        )
    with allure.step("Запуск билд конфигурации с добавлением шагов"):
        run_build_with_step = RunBuildWithStep(browser, build_conf_id)
        run_build_with_step.run_build_conf_with_step()
        run_build_with_step.check_url_change(build_conf_id)
    with allure.step("Проверка счетчика 'Queue' в header"):
        project_creation_browser.header.check_queue_count_through_header_button("1")
    with allure.step(
        "Отправка запроса на проверку количества билд конфигураций в очереди для запуска"
    ):
        get_build_conf_run_response = (
            super_admin.api_manager.build_conf_api.check_query_with_build_conf().text
        )
    with allure.step(
        "Проверка соответствия параметров модели ответа запуска билд конфигурации с отправленными данными"
    ):
        build_run_response = BuildConfRunStatusModel.model_validate_json(
            get_build_conf_run_response
        )
        assert (
            build_run_response.count == 0
        ), f"build was expected to be out of the query=0, but it is still here: query={build_run_response.count}"
