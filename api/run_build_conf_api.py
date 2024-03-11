from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class RunBuildConfAPI(CustomRequester):

    def run_build_conf(self, run_build_data, expected_status=HTTPStatus.OK):
        # Метод для отправки запроса для запуска билд конфигурации
        return self.send_request("POST", "/app/rest/buildQueue", data=run_build_data, expected_status=expected_status)

    def check_status_build_conf(self, build_conf_id, expected_status=HTTPStatus.OK):
        # Метод для запроса списка билд конфигураций в очереди
        return self.send_request("GET", f"/app/rest/buildQueue?locator=buildType(id:{build_conf_id})", expected_status=expected_status)

    def cancel_run_build_conf(self, build_conf_data, build_conf_in_id, expected_status=HTTPStatus.OK):
        # Метод для запроса отмены билда в очереди
        return self.send_request("POST", f"/app/rest/buildQueue/id:{build_conf_in_id}", data=build_conf_data, expected_status=expected_status)

    def check_query_with_build_conf(self, expected_status=HTTPStatus.OK):
        # Метод запроса списка билд конфигураций в очереди
        return self.send_request("GET", f"/app/rest/buildQueue", expected_status=expected_status)








