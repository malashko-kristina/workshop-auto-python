from http import HTTPStatus
from custom_requester.custom_requester import CustomRequester


class AgentAPI(CustomRequester):

    def check_amount_of_authorized_agents(self, expected_status=HTTPStatus.OK):
        # Метод для отправки запроса на получение списка активных агентов
        return self.send_request("GET",
                                 "/app/rest/agents?locator=connected:true,authorized:true",
                                 expected_status=expected_status)