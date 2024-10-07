from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class ProjectAPI(CustomRequester):

    def create_project(self, project_data, expected_status=HTTPStatus.OK):
        # Method for sending a request to create a project
        return self.send_request("POST",
                                 "/app/rest/projects",
                                 data=project_data,
                                 expected_status=expected_status)

    def create_copy_project(self, project_data, expected_status=HTTPStatus.OK):
        # Method for sending a request to copy a project
        return self.send_request("POST",
                                 "/app/rest/projects",
                                 data=project_data,
                                 expected_status=expected_status)

    def get_project(self, expected_status=HTTPStatus.OK):
        # Method for sending a request to check that the project was created
        return self.send_request("GET",
                                 "/app/rest/projects",
                                 expected_status=expected_status)

    def get_project_by_locator(self, locator, expected_status=HTTPStatus.OK):
        # Method for retrieving information about a specific project
        return self.send_request("GET",
                                 f"/app/rest/projects/{locator}",
                                 expected_status=expected_status)

    def delete_project(self, project_id,
                       expected_status=HTTPStatus.NO_CONTENT):
        # Method for deleting a project
        return self.send_request("DELETE",
                                 f"/app/rest/projects/id:{project_id}",
                                 expected_status=expected_status)

    def clean_up_project(self, created_project_id):
        # Logic for checking project creation and deletion
        self.delete_project(created_project_id)
        get_response = self.get_project().json()
        project_ids = [project.get("id", {})
                       for project in get_response.get("project", [])]
        assert created_project_id not in project_ids, \
            "The ID of the created project is found in the project list after deletion"
