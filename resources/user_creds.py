import os
from dotenv import load_dotenv


load_dotenv()  # Берет переменную из файла .env под именем 'SUPER_USER_TOKEN'


class SuperAdminCreds:
    """
    Креды супер админа. Для авторизации в TeamCity под супер админом оставляется пустым username, а пароль - токен и логов
    контейнера
    """
    USERNAME = ''
    PASSWORD = os.getenv('SUPER_USER_TOKEN')


class UsualUserCreds:
    """
    Креды для обычного юзера
    """
    USER_LOGIN = os.getenv("USER_LOGIN")
    USER_PASSWORD = os.getenv("USER_PASSWORD")