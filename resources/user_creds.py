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
