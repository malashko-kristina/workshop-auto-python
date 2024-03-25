import copy
import time
from http import HTTPStatus
import pytest
import allure
from data.project_data import ProjectResponseModel
from data.build_conf_data import BuildResponseModel
from data.run_build_data import BuildRunResponseModel, BuildConfRunStatusModel, \
    BuildRunCancelResponseModel


class TestRunBuildConfSeveralTimes:

        @allure.feature('Управление запуском билд конфигураций')
        @allure.story('Отправка запроса на запуск одной и той же билд конфигурации несколько раз с разными ролями')
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.link('https://example.com/docs/create_project', name='Документация')
        @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
        @allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс-23')
        @allure.title('Проверка запуска одной и той же билд конфигурации несколько раз')
        @allure.description('Тест проверяет запуск одной и той билд конфигурации несколько раз.')

        def test_run_build_conf_several_times_with_roles(self, super_admin, user_create, project_data, build_conf_data, build_conf_run_data):

            with allure.step('Отправка запроса на создание проекта'):
                project_data_1 = project_data
                create_project_response = super_admin.api_manager.project_api.create_project(project_data_1.model_dump()).text
            with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
                project_model_response = ProjectResponseModel.model_validate_json(create_project_response)
            with pytest.assume:
                assert project_model_response.id == project_data_1.id, \
                    f"expected project id= {project_data_1.id}, but '{project_model_response.id}' given"
            with pytest.assume:
                assert project_model_response.parentProjectId == project_data_1.parentProject["locator"], \
                    (f"expected parent project id= {project_data_1.parentProject['locator']},"
                     f" but '{project_model_response.parentProjectId}' given in response")
            with allure.step("Отправка запроса на создание билд конфигурации"):
                build_conf_data_1 = build_conf_data
                build_config_response = super_admin.api_manager.build_conf_api.create_build_conf(build_conf_data_1.model_dump()).text
            with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
                build_conf_model_response = BuildResponseModel.model_validate_json(build_config_response)
            with pytest.assume:
                assert build_conf_model_response.id == build_conf_data_1.id, \
                    f"expected build conf id= {build_conf_data_1.id}, but '{build_conf_model_response.id}' given"
            with allure.step('Отправка запроса на запуск билд конфигурации'):
                build_conf_run_data_1 = build_conf_run_data
                build_run_response = super_admin.api_manager.run_build_conf_api.run_build_conf(build_conf_run_data_1.model_dump()).text
                time.sleep(180)
            with allure.step("Проверка соответствия параметров запущенной билд конфигурации с отправленными данными"):
                build_run_model_response = BuildRunResponseModel.model_validate_json(build_run_response)
            with pytest.assume:
                assert build_run_model_response.state == "queued", \
                    f"build was expected to be run= {build_run_model_response.state} should be queued, but it is not in a query= {build_run_model_response.state}"
            with allure.step("Проверка количества билд конфигураций в очереди для запуска"):
                get_build_conf_run_response = super_admin.api_manager.run_build_conf_api.check_query_with_build_conf().text
            with allure.step("Проверка соответствия параметров запущенных билд конфигураций с отправленными данными"):
                build_conf_run_check_model_response = BuildConfRunStatusModel.model_validate_json(get_build_conf_run_response)
            with pytest.assume:
                assert build_conf_run_check_model_response.count == 0, \
                    f"build was expected to be out of the query=0, but it is still here: query={build_conf_run_check_model_response.count}"
            with allure.step("Отправка запроса на повторный запуск билд конфигурации"):
                build_conf_run_data_2 = copy.deepcopy(build_conf_run_data)
                build_run_response = super_admin.api_manager.run_build_conf_api.run_build_conf(build_conf_run_data_2.model_dump()).text
                time.sleep(180)
            with allure.step("Проверка соответствия параметров запущенной билд конфигурации с отправленными данными"):
                build_run_model_response = BuildRunResponseModel.model_validate_json(build_run_response)
            with pytest.assume:
                assert build_run_model_response.state == "queued", \
                        f"build was expected to be run= {build_run_model_response.state} should be queued, but it is not in a query= {build_run_model_response.state}"
            with allure.step("Проверка количества билд конфигураций в очереди для запуска"):
                    get_build_conf_run_response = super_admin.api_manager.run_build_conf_api.check_query_with_build_conf().text
            with allure.step("Проверка соответствия параметров запущенных билд конфигураций с отправленными данными"):
                    build_conf_run_check_model_response = BuildConfRunStatusModel.model_validate_json(get_build_conf_run_response)
            with pytest.assume:
                assert build_conf_run_check_model_response.count == 0, \
                        f"build was expected to be out of the query=0, but it is still here: query={build_conf_run_check_model_response.count}"

class TestRunBuildConfWithWrongBuildConfId:

        @allure.feature('Управление запуском билд конфигураций')
        @allure.story('Отправка запроса на запуск несуществующей билд конфигурации с разными ролями')
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.link('https://example.com/docs/create_project', name='Документация')
        @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
        @allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс-24')
        @allure.title('Проверка запуска несуществующей билд конфигурации')
        @allure.description('Негативный тест проверяет запуск несуществующей билд конфигурации.')

        def test_run_build_conf_with_wrong_build_id_with_roles(self, super_admin, user_create, project_data, build_conf_data, build_conf_run_data_with_wrong_build_conf_id):

            with allure.step('Отправка запроса на создание проекта'):
                project_data_1 = project_data
                create_project_response = super_admin.api_manager.project_api.create_project(project_data_1.model_dump()).text
            with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
                project_model_response = ProjectResponseModel.model_validate_json(create_project_response)
            with pytest.assume:
                assert project_model_response.id == project_data_1.id, \
                    f"expected project id= {project_data_1.id}, but '{project_model_response.id}' given"
            with pytest.assume:
                assert project_model_response.parentProjectId == project_data_1.parentProject["locator"], \
                    (f"expected parent project id= {project_data_1.parentProject['locator']},"
                     f" but '{project_model_response.parentProjectId}' given in response")
            with allure.step("Отправка запроса на создание билд конфигурации"):
                build_conf_data_1 = build_conf_data
                build_config_response = super_admin.api_manager.build_conf_api.create_build_conf(build_conf_data_1.model_dump()).text
            with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
                build_conf_model_response = BuildResponseModel.model_validate_json(build_config_response)
            with pytest.assume:
                assert build_conf_model_response.id == build_conf_data_1.id, \
                    f"expected build conf id= {build_conf_data_1.id}, but '{build_conf_model_response.id}' given"
            with allure.step('Отправка запроса на запуск билд конфигурации'):
                build_conf_run_data_1 = build_conf_run_data_with_wrong_build_conf_id
                build_run_response = super_admin.api_manager.run_build_conf_api.run_build_conf(build_conf_run_data_1.model_dump(), expected_status=HTTPStatus.NOT_FOUND).text
            with pytest.assume:
                assert f"NotFoundException: No build type nor template is found by id '{build_conf_run_data_1.buildType.id}'" in build_run_response


class TestRunBuildConfAndCancel:

        @allure.feature('Управление запуском билд конфигураций')
        @allure.story('Отправка запроса на отмену запущенной билд конфигурации с разными ролями')
        @allure.severity(allure.severity_level.CRITICAL)
        @allure.link('https://example.com/docs/create_project', name='Документация')
        @allure.issue('https://issue.tracker/project/123', name='Баг-трекер')
        @allure.testcase('https://testcase.manager/testcase/456', name='Тест-кейс-25')
        @allure.title('Проверка отмена запущенной билд конфигурации')
        @allure.description('Тест проверяет отмену запущенной билд конфигурации.')

        def test_run_build_conf_and_cancel_with_roles(self, super_admin, user_create, project_data, build_conf_data, build_conf_run_data, build_conf_run_cancel):

            with allure.step('Отправка запроса на создание проекта'):
                project_data_1 = project_data
                create_project_response = super_admin.api_manager.project_api.create_project(project_data_1.model_dump()).text
            with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
                project_model_response = ProjectResponseModel.model_validate_json(create_project_response)
            with pytest.assume:
                assert project_model_response.id == project_data_1.id, \
                    f"expected project id= {project_data_1.id}, but '{project_model_response.id}' given"
            with pytest.assume:
                assert project_model_response.parentProjectId == project_data_1.parentProject["locator"], \
                    (f"expected parent project id= {project_data_1.parentProject['locator']},"
                     f" but '{project_model_response.parentProjectId}' given in response")
            with allure.step("Отправка запроса на создание билд конфигурации"):
                build_conf_data_1 = build_conf_data
                build_config_response = super_admin.api_manager.build_conf_api.create_build_conf(build_conf_data_1.model_dump()).text
            with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
                build_conf_model_response = BuildResponseModel.model_validate_json(build_config_response)
            with pytest.assume:
                assert build_conf_model_response.id == build_conf_data_1.id, \
                    f"expected build conf id= {build_conf_data_1.id}, but '{build_conf_model_response.id}' given"
            with allure.step('Отправка запроса на запуск билд конфигурации'):
                build_conf_run_data_1 = build_conf_run_data
                build_run_response = super_admin.api_manager.run_build_conf_api.run_build_conf(build_conf_run_data_1.model_dump()).text
            with allure.step("Проверка соответствия параметров запущенной билд конфигурации с отправленными данными"):
                build_run_model_response = BuildRunResponseModel.model_validate_json(build_run_response)
            with pytest.assume:
                assert build_run_model_response.state == "queued", \
                    f"build was expected to be run= {build_run_model_response.state} should be queued, but it is not in a query= {build_run_model_response.state}"
            with allure.step("Отправка запроса на отмену запущенной билд конфигурации"):
                build_in_id = build_run_model_response.id
                build_conf_run_cancel_1 = build_conf_run_cancel
                build_run_cancel_response = super_admin.api_manager.run_build_conf_api.cancel_run_build_conf(build_conf_run_cancel_1.model_dump(), build_in_id).text
            with allure.step("Проверка соответствия параметров отмены запущенной билд конфигурации с отправленными данными"):
                build_run_cancel_model_response = BuildRunCancelResponseModel.model_validate_json(build_run_cancel_response)
            with pytest.assume:
                assert build_run_cancel_model_response.statusText == "Canceled", \
                f"build was expected to be cancelled= {build_run_cancel_model_response.statusText}, but it is not"





















