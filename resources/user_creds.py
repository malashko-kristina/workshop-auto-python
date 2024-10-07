import os
from dotenv import load_dotenv


load_dotenv()


class SuperAdminCreds:
    """
    Super admin credentials. To log in to TeamCity as a super admin,
    leave the username blank, and the password
    is the token and logs of the container
    """
    USERNAME = ''
    PASSWORD = os.getenv('SUPER_USER_TOKEN')


class UsualUserCreds:
    """
    Creds for the average user
    """
    USER_LOGIN = os.getenv("USER_LOGIN")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
