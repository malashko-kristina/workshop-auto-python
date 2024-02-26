from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester

class BuildConfAPI(CustomRequester):

    #Метод для отправки запроса на создание билд конфигурации
    def create_build_conf(self, build_conf_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildTypes", data=build_conf_data, expected_status=expected_status)

    #Метод по отправки запроса для запуска билд конфигурации
    def run_build_conf(self, run_build_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/buildQueue", data=run_build_data, expected_status=expected_status)

    #Метод для запроса списка билд конфигураций в очереди по определенной билд конфигурации
    def check_status_build_conf(self, build_conf_id, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/buildQueue?locator=buildType(id:{build_conf_id})", expected_status=expected_status)

   #Метод запроса списка билд конфигураций в очереди
    def check_query_with_build_conf(self, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/buildQueue", expected_status=expected_status)

    #Метод по отправки запроса по получению инфы о конкретном билде
    def get_build_conf(self, build_conf_id, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/buildTypes/id:{build_conf_id}", expected_status=expected_status)

    #Метод для удаления билд конфигурации
    def delete_build_conf(self, build_conf_id, expected_status=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/buildTypes/id:{build_conf_id}", expected_status=expected_status)

    #Метод по копированию билд конфигурации
    def create_build_conf_copy(self, build_conf_data, project_id, expected_status=HTTPStatus.OK):
        return self.send_request("POST", f"/app/rest/projects/{project_id}/buildTypes", data=build_conf_data, expected_status=expected_status)


    #Логика для проверки создания билд конфигурации и его удаления
    def clean_up_build(self, build_conf_id):
        self.delete_build_conf(build_conf_id)
        get_build_conf_response = self.check_query_with_build_conf().json()
        #извлекаем все айдишники из нашего ответа, если ничего не найдет, то вернет пустой словарь
        build_conf_ids = [build_conf.get("id", {}) for build_conf in get_build_conf_response.get("build", [])]
        assert build_conf_id not in build_conf_ids, "ID созданного билд конфига найдет в списке билд конфигов после удаления"







