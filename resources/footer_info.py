import os
from dotenv import load_dotenv


load_dotenv()


class BuildVersion:
    """
    Версия билда, указанная в футере
    """
    BUILD_VERSION = os.getenv("BUILD_VERSION")

    @classmethod
    def build_version(cls):
        return (f"[title=\"Node id: MAIN_SERVER\"]"
                f" >> text=\"{cls.BUILD_VERSION}\"")


class AppName:
    """
    Имя приложения, указанное в футере
    """
    APP_NAME = os.getenv('APPLICATION_NAME')

    @classmethod
    def app_name(cls):
        return (f"[title=\"Node id: MAIN_SERVER\"]"
                f" >> text=\"{cls.APP_NAME}\"")
