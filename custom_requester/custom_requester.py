import logging
import os
from http import HTTPStatus
from enums.host import BASE_URL
from swagger_coverage_py.configs import IS_DISABLED
from swagger_coverage_py.request_schema_handler import RequestSchemaHandler
from swagger_coverage_py.uri import URI


class CustomCoverageListener:
    def __init__(
            self,
            session,
            method,
            base_url,
            endpoint,
            uri_params,
            **kwargs
    ):
        self.__uri = URI(base_url, "", endpoint, **uri_params)
        self.response = session.request(method, self.__uri.full, **kwargs)
        if not IS_DISABLED:
            RequestSchemaHandler(
                self.__uri, method, self.response, kwargs
            ).write_schema()


class CustomRequester:
    base_headers = dict(
        {"Content-Type": "application/json", "Accept": "application/json"}
    )  # Dictionary with basic headers

    def __init__(self, session):
        self.session = session
        self.base_url = BASE_URL
        self.logger = logging.getLogger(
            __name__
        )  # Activate the logger by defining the logger attribute in the class

    def send_request(
        self,
        method,
        endpoint,
        data=None,
        expected_status=HTTPStatus.OK,
        need_logging=True,
    ):
        """
        :param method: Request method
        :param endpoint: Endpoint to concatenate with BASE_URL in the "url" variable
        :param data: Request body. Default is empty to allow passing NO_CONTENT responses
        :param expected_status: Expected response status. If a status other than SC_OK is expected, pass it in the API class method
        :param need_logging: Flag for logging. Default is True
        :return: Returns the response object
        """
        if endpoint == "/authenticationTest.html?csrf":
            url = f"{self.base_url}{endpoint}"
            response = self.session.request(method, url, json=data)
        else:
            request_kwargs = {
                "json": data,
            }
            coverage_listener = CustomCoverageListener(
                session=self.session,
                method=method,
                base_url=self.base_url,
                endpoint=endpoint,
                uri_params={},
                **request_kwargs,
            )
            response = coverage_listener.response
        if need_logging:
            self.log_request_and_response(response)
        if response.status_code != expected_status:
            raise ValueError(f"Unexpected status code:{response.status_code}")
        return response

    def _update_session_headers(
        self, **kwargs
    ):
        self.headers = self.base_headers.copy()
        self.headers.update(kwargs)  # Обновляется значение словаря
        self.session.headers.update(self.headers)

    def log_request_and_response(self, response):
        """

        Logging requests and responses. Logging settings are described in pytest.ini.
        Transforms output into curl-like format (-H for headers, -d for body)

        :param response: Response object obtained from the "send_request" method

        """
        try:
            request = response.request
            GREEN = "\033[32m"
            RED = "\033[31m"
            RESET = "\033[0m"  # Reset color to default
            headers = "\\\n".join(
                [
                    f"-H '{headers}: {value}'"
                    for headers, value in request.headers.items()
                ]
            )
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, "body") and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode("utf-8")
            body = f"-d '{body}' \n" if body != "{}" else ""

            self.logger.info(
                f"{GREEN} {full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = (
                response.ok
            )
            response_data = response.text

            if not is_success:
                self.logger.info(
                    f"\tRESPONSE:\nSTATUS_CODE: {RED}{response_status}"
                    f"{RESET}\nDATA: {RED}{response_data}{RESET}"
                )

        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")
