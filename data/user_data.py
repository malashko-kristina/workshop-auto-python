from enums.roles import Roles
from utilis.data_generator import DataGenerator


class UserData:
    #Метод, генерирующий данные юзера
    @staticmethod
    def create_user_data(role=Roles.SYSTEM_ADMIN.value, scope="g"):
        return {
            "username": DataGenerator.fake_name(),
            "password": DataGenerator.fake_project_id(),
            "email": DataGenerator.fake_emaiL(),
            "roles": {
                "role":[
                    {
                           "roleId": role,
                           "scope": scope,
                    }
                ]
            }
        }



