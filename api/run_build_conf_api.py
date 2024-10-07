from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class RunBuildConfAPI(CustomRequester):

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
        # Method for requesting the list of build configurations in the queue
        return self.send_request(
            "GET",
            f"/app/rest/buildQueue?locator=buildType"
            f"(id:{build_conf_id})",
            expected_status=expected_status,
        )

    def cancel_run_build_conf(
        self, build_conf_data, build_conf_in_id,
            expected_status=HTTPStatus.OK
    ):
        # Method for requesting the cancellation of a build in the queue
        return self.send_request(
            "POST",
            f"/app/rest/buildQueue/id:{build_conf_in_id}",
            data=build_conf_data,
            expected_status=expected_status,
        )

    def check_query_with_build_conf(self, expected_status=HTTPStatus.OK):
        # Method for requesting the list of build configurations in the queue
        return self.send_request(
            "GET", "/app/rest/buildQueue",
            expected_status=expected_status
        )
