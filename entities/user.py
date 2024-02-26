from api.api_manager import ApiManager
from enums.roles import Roles


class Role:
    def __init__(self, role_id, scope="g", href=None):
        if role_id not in Roles.__members__:
            raise ValueError(f"Invalid role: {role_id}")
        self.role_id = role_id
        self.scope = scope
        self.href = href


#Этот класс модулирует пользователя система и инкапсулирует его основные атрибуты (имя, пароль и так далее)
# + предоставление методов для работы с этими данными

class User:
    def __init__(self, username: str, password: str, session: ApiManager, roles: list,  **kwargs): #это нотации, которые описывают, какой тип данных у каждого аргумента
        self.username = username
        self.password = password
        self.email = None #вот сюда надо будет подставить фейковый емейл
        self.roles = roles
        self.groups = None
        self.api_manager = session #api_manager это экземпляр ApiManager, назвали так, чтобы не было путаницы ????

     #Создаем метод, который возвращает креды, но поскольку нельзя, чтобы его кто-то мог редактировать, мы к нему даем
    #доступ только для чтения (обращаемся теперь к нему через точку)

    @property
    def creds(self):
        return self.username, self.password
