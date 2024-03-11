from api.auth_api import AuthAPI
from api.build_conf_api import BuildConfAPI
from api.project_api import ProjectAPI
from api.run_build_conf_api import RunBuildConfAPI
from api.user_api import UserAPI


class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.project_api = ProjectAPI(session)
        self.user_api = UserAPI(session)
        self.build_conf_api = BuildConfAPI(session)
        self.run_build_conf_api = RunBuildConfAPI(session)

    def close_session(self):
        self.session.close()

