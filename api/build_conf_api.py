from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class BuildConfAPI(CustomRequester):

    def create_build_conf(self, build_conf_data,
                          expected_status=HTTPStatus.OK):
        # Method for sending a request to create a build configuration
        return self.send_request(
            "POST",
            "/app/rest/buildTypes",
            data=build_conf_data,
            expected_status=expected_status,
        )

    def run_build_conf(self, run_build_data,
                       expected_status=HTTPStatus.OK):
        # Method for sending a request to trigger a build configuration
        return self.send_request(
            "POST",
            "/app/rest/buildQueue",
            data=run_build_data,
            expected_status=expected_status,
        )

    def check_status_build_conf(self, build_conf_id,
                                expected_status=HTTPStatus.OK):
        # Method to request the list of build configurations in the queue by build configuration ID
        return self.send_request(
            "GET",
            f"/app/rest/buildQueue?locator=buildType"
            f"(id:{build_conf_id})",
            expected_status=expected_status,
        )

    def check_query_with_build_conf(self, expected_status=HTTPStatus.OK):
        # Method to request the list of build configurations in the queue
        return self.send_request(
            "GET", "/app/rest/buildQueue",
            expected_status=expected_status
        )

    def get_build_conf(self, build_conf_id, expected_status=HTTPStatus.OK):
        # Method for sending a request to retrieve information about a specific build
        return self.send_request(
            "GET",
            f"/app/rest/buildTypes/id:{build_conf_id}",
            expected_status=expected_status,
        )

    def delete_build_conf(self, build_conf_id,
                          expected_status=HTTPStatus.NO_CONTENT):
        # Method for deleting a build configuration
        return self.send_request(
            "DELETE",
            f"/app/rest/buildTypes/id:{build_conf_id}",
            expected_status=expected_status,
        )

    def create_build_conf_copy(
        self, build_conf_data, project_id,
            expected_status=HTTPStatus.OK
    ):
        # Method for copying a build configuration
        return self.send_request(
            "POST",
            f"/app/rest/projects/{project_id}/buildTypes",
            data=build_conf_data,
            expected_status=expected_status,
        )

    def clean_up_build(self, build_conf_id):
        # Logic for checking the creation of a build configuration and its deletion
        self.delete_build_conf(build_conf_id)
        get_response = self.check_query_with_build_conf().json()
        build_conf_ids = [
            build_conf.get("id", {}) for build_conf
            in get_response.get("build", [])
        ]
        assert (
            build_conf_id not in build_conf_ids
        ), ("The ID of the created build configuration will be found in the"
            " list of build configurations after deletion.")
