from http import HTTPStatus

from custom_requester.custom_requester import CustomRequester

class ProjectAPI(CustomRequester):
    
    #Метод для отправки запроса на создание проекта
    def create_project(self, project_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/projects", data=project_data, expected_status=expected_status)

    #Метод для отправки запроса на копирование проекта
    def create_copy_project(self, project_data, expected_status=HTTPStatus.OK):
        return self.send_request("POST", "/app/rest/projects", data=project_data, expected_status=expected_status)

    #Метод для отправки запроса для проверки, что проект создался,
    #используем точно такой же эндпоинт, так как будет проверять по всему списку созданных проектов

    def get_project(self, expected_status=HTTPStatus.OK):
        return self.send_request("GET", "/app/rest/projects", expected_status=expected_status)

    def get_project_by_locator(self, locator, expected_status=HTTPStatus.OK):
        return self.send_request("GET", f"/app/rest/projects/{locator}", expected_status=expected_status)

    #Метод для удаления проекта
    def delete_project(self, project_id, expected_status=HTTPStatus.NO_CONTENT):
        return self.send_request("DELETE", f"/app/rest/projects/id:{project_id}", expected_status=expected_status)

    #Логика для проверки создания проекта и его удаления
    def clean_up_project(self, created_project_id):
        self.delete_project(created_project_id)
        get_projects_response = self.get_project().json() #
        #извлекаем все айдишники из нашего ответа, если ничего не найдет, то вернет пустой словарь
        project_ids = [project.get("id", {}) for project in get_projects_response.get("project", [])]
        assert created_project_id not in project_ids, "ID созданного проекта найдет в списке проектов после удаления"








