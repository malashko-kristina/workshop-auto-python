import pytest
import allure
import time
from data.project_data import ProjectResponseModel
from data.build_conf_data import BuildResponseModel
from data.run_build_data import BuildRunResponseModel, BuildConfRunStatusModel


class TestProjectCreate:

    @allure.feature('Управление проектами и билд конфигурациями')
    @allure.story('Создание проекта и билд конфигурации с последующем для нее запуском под разными ролями')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link('https://example.com/docs/create_project', name='Документация')
    @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
    @allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс')
    @allure.title('Проверка юзер флоу по созданию проекта, билд конфигурации и ее запуску')
    @allure.description('Тест проверяет создание нового проекта и его появление в общем списке проектов.')
    def test_user_critical_flow_with_roles(self, super_admin, user_create, project_data, build_conf_data, build_conf_run_data):

        with allure.step('Отправка запроса на создание проекта'):
            project_data_1 = project_data
            create_project_response = super_admin.api_manager.project_api.create_project(
                project_data_1.model_dump()).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            project_model_response = ProjectResponseModel.model_validate_json(
                create_project_response)
        with pytest.assume:
            assert project_model_response.id == project_data_1.id, \
                f"expected project id= {project_data_1.id}, but '{project_model_response.id}' given"
        with pytest.assume:
            assert project_model_response.parentProjectId == project_data_1.parentProject["locator"], \
                (f"expected parent project id= {project_data_1.parentProject['locator']},"
                 f" but '{project_model_response.parentProjectId}' given in response")
        with allure.step("Проверка нахождения id созданного проекта в общем списке проектов"):
            get_project_response = super_admin.api_manager.project_api.get_project_by_locator(
                project_data_1.id).text
        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            created_model_project_response = ProjectResponseModel.model_validate_json(
                get_project_response)
        with pytest.assume:
            assert created_model_project_response.id == project_data_1.id, f"There is no project with {
                project_data_1.id} id"
        with allure.step("Отправка запроса на создание билд конфигурации"):
            build_conf_data_1 = build_conf_data
            build_config_response = super_admin.api_manager.build_conf_api.create_build_conf(
                build_conf_data_1.model_dump()).text
        with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
            build_conf_model_response = BuildResponseModel.model_validate_json(
                build_config_response)
        with pytest.assume:
            assert build_conf_model_response.id == build_conf_data_1.id, \
                f"expected build conf id= {build_conf_data_1.id}, but '{
                    build_conf_model_response.id}' given"
        with allure.step("Проверка нахождения id созданной билд конфигурации в общем списке билд конфигураций"):
            get_build_conf_response = super_admin.api_manager.build_conf_api.get_build_conf(
                build_conf_data_1.id).text
        with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
            build_conf_model_response_1 = BuildResponseModel.model_validate_json(
                get_build_conf_response)
        with pytest.assume:
            assert build_conf_model_response_1.id == build_conf_data_1.id, \
                f"expected build conf id= {build_conf_data_1.id}, but '{
                    build_conf_model_response_1.id}' given"
        with allure.step("Отправка запроса на запуск созданной билд конфигурации с временем ожидания после запроса 10 секунд"):
            build_conf_run_data_1 = build_conf_run_data
            build_run_response = super_admin.api_manager.run_build_conf_api.run_build_conf(
                build_conf_run_data_1.model_dump()).text
            time.sleep(15)
        with allure.step("Проверка соответствия параметров модели запуска билд конфигурации с отправленными данными"):
            build_run_model_response = BuildRunResponseModel.model_validate_json(
                build_run_response)
        with pytest.assume:
            assert build_run_model_response.state == "queued", \
                f"build was expected to be run= {build_run_model_response.state} should be queued, but it is not in a query= {
                    build_run_model_response.state}"
        with allure.step("Отправка запроса на проверку количества билд конфигураций в очереди для запуска"):
            get_build_conf_run_response = super_admin.api_manager.build_conf_api.check_query_with_build_conf().text
            time.sleep(15)
        with allure.step("Проверка соответствия параметров модели ответа запуска билд конфигурации с отправленными данными"):
            build_conf_run_check_model_response = BuildConfRunStatusModel.model_validate_json(
                get_build_conf_run_response)
        with pytest.assume:
            assert build_conf_run_check_model_response.count == 0, \
                f"build was expected to be out of the query=0, but it is still here: query={
                    build_conf_run_check_model_response.count}"
