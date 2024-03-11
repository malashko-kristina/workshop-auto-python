from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class BuildConfAPI(CustomRequester):

    def create_build_conf(self, build_conf_data, expected_status=HTTPStatus.OK):
        # Метод для отправки запроса на создание билд конфигурации
        return self.send_request("POST", "/app/rest/buildTypes", data=build_conf_data, expected_status=expected_status)

    def run_build_conf(self, run_build_data, expected_status=HTTPStatus.OK):
        # Метод для отправки запроса для запуска билд конфигурации
        return self.send_request("POST", "/app/rest/buildQueue", data=run_build_data, expected_status=expected_status)

    def check_status_build_conf(self, build_conf_id, expected_status=HTTPStatus.OK):
        # Метод для запроса списка билд конфигураций в очереди по определенной билд конфигурации
        return self.send_request("GET", f"/app/rest/buildQueue?locator=buildType(id:{build_conf_id})", expected_status=expected_status)

    def check_query_with_build_conf(self, expected_status=HTTPStatus.OK):
        # Метод запроса списка билд конфигураций в очереди
        return self.send_request("GET", f"/app/rest/buildQueue", expected_status=expected_status)

    def get_build_conf(self, build_conf_id, expected_status=HTTPStatus.OK):
        # Метод для отправки запроса по получению инфы о конкретном билде
        return self.send_request("GET", f"/app/rest/buildTypes/id:{build_conf_id}", expected_status=expected_status)

    def delete_build_conf(self, build_conf_id, expected_status=HTTPStatus.NO_CONTENT):
        # Метод для удаления билд конфигурации
        return self.send_request("DELETE", f"/app/rest/buildTypes/id:{build_conf_id}", expected_status=expected_status)

    def create_build_conf_copy(self, build_conf_data, project_id, expected_status=HTTPStatus.OK):
        # Метод по копированию билд конфигурации
        return self.send_request("POST", f"/app/rest/projects/{project_id}/buildTypes", data=build_conf_data, expected_status=expected_status)

    def clean_up_build(self, build_conf_id):
        # Логика для проверки создания билд конфигурации и его удаления
        self.delete_build_conf(build_conf_id)
        get_build_conf_response = self.check_query_with_build_conf().json()
        build_conf_ids = [build_conf.get("id", {}) for build_conf in get_build_conf_response.get("build", [])]
        assert build_conf_id not in build_conf_ids, "ID созданного билд конфига найдет в списке билд конфигов после удаления"







