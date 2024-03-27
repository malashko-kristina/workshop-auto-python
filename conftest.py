import pytest
import requests
from api.api_manager import ApiManager
from data.build_conf_data import BuildConfData
from data.project_data import ProjectData
from data.run_build_data import BuildRunData
from data.user_data import UserData
from entities.user import User, Role
from enums.browser import BROWSERS
from enums.roles import Roles
from resources.user_creds import SuperAdminCreds
from utilis.browser_setup import BrowserSetup
from utilis.data_generator import DataGenerator


@pytest.fixture(params=BROWSERS)
def browser(request):
    playwright, browser, context, page = BrowserSetup.setup(browser_type=request.param)
    yield page
    BrowserSetup.teardown(context, browser, playwright)


@pytest.fixture(scope='session')
def one_browser():
    playwright, browser, context, page = BrowserSetup.setup(browser_type="chromium")
    yield page
    BrowserSetup.teardown(context, browser, playwright)


@pytest.fixture
def user_session():
    user_pool = []
    """ 
    Создаем сессии созданных пользователей, которые мы потом будем удалять.
    Функция _create_user_session: Это вложенная функция, которая создает новую HTTP-сессию с помощью requests.Session(),
    оборачивает ее в ApiManager для удобства управления API-вызовами, добавляет созданный объект сессии в user_pool и
    возвращает его. Эта функция позволяет создавать отдельные сессии для разных пользователей при необходимости.
    """
    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session
    """
    Ключевое слово yield возвращается из фикстуры с функцией _create_user_session. Это означает, что в тестах,
    где используется эта фикстура, будет предоставлена возможность создавать пользовательские сессии вызовом
    _create_user_session().
    При этом выполнение кода после yield отложено до момента завершения скоупа фикстуры.
    """
    yield _create_user_session

    """
    Очистка сессий: После того как тесты, использующие эту фикстуру, завершат своё выполнение, pytest продолжит
    выполнение кода после yield. В этой части кода происходит итерация по всем сессиям в user_pool с вызовом
    метода close_session() для каждой сессии. Этот шаг важен для корректного закрытия всех сессий и освобождения
    ресурсов, ассоциированных с ними.
    """
    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, new_session, ["SUPER_ADMIN", "g"])  # В класс юзер создаем новый объект
    super_admin.api_manager.auth_api.auth_and_get_csrf(super_admin.creds)
    return super_admin


@pytest.fixture(params=[Roles.SYSTEM_ADMIN, Roles.PROJECT_ADMIN, Roles.PROJECT_DEVELOPER, Roles.PROJECT_VIEWER])
def user_create(user_session, super_admin):
    # Фикстура, создающая юзера от имени супер админа
    created_users_pool = []

    def _user_create(role):
        user_data = UserData.create_user_data(role, scope="g")
        super_admin.api_manager.user_api.create_user(user_data)
        new_session = user_session()
        created_users_pool.append(user_data['username'])
        return User(user_data['username'], user_data['password'], new_session, [Role(role)])

    yield _user_create

    for username in created_users_pool:
        super_admin.api_manager.user_api.delete_user(username)

@pytest.fixture
def project_data_create(super_admin):
    project_id_pool = []

    def _project_data():
        project = ProjectData.create_project_data_with_data()
        project_id_pool.append(project.id)
        return project

    yield _project_data

    for project_id in project_id_pool:
        super_admin.api_manager.project_api.clean_up_project(project_id)


@pytest.fixture(params=[DataGenerator.fake_build_id()])
def project_data(super_admin, request):
    project_id_pool = []

    def _create_project_data():
        name = request.param
        project = ProjectData.create_project_data_with_correct_data(name)
        project_id_pool.append(project.id)
        return project

    yield _create_project_data()

    for project_id in project_id_pool:
        super_admin.api_manager.project_api.clean_up_project(project_id)

@pytest.fixture
def project_data_first_project(super_admin):
    project_id_pool = []

    def _create_project_data_first_project():
        project = ProjectData.create_first_project_data_with_correct_data()
        project_id_pool.append(project.id)
        return project

    yield _create_project_data_first_project

    for project_id in project_id_pool:
        super_admin.api_manager.project_api.clean_up_project(project_id)

@pytest.fixture
def project_copy_data(super_admin, project_data):
    project_id_copy_pool = []

    def _create_project_copy_data():
        project_copy = ProjectData.create_project_data_copy(project_data.id)
        project_id_copy_pool.append(project_copy.id)
        return project_copy

    yield _create_project_copy_data()

    for project_copy_id in project_id_copy_pool :
        super_admin.api_manager.project_api.clean_up_project(project_copy_id)


@pytest.fixture
def project_copy_data_with_another_source_project(super_admin):
        project_copy = ProjectData.create_project_data_copy_with_another_source_project
        yield project_copy


@pytest.fixture
def project_data_without_deleting(super_admin):
        project = ProjectData.create_project_data_with_data
        yield project


@pytest.fixture
def project_data_with_empty_id(super_admin):
        project = ProjectData.create_project_data_with_empty_id
        yield project


@pytest.fixture(params=[DataGenerator.incorrect_id_1(), DataGenerator.incorrect_id_2(),DataGenerator.incorrect_id_3()])
def project_data_with_invalid_ids(request, super_admin):
    ids = request.param
    project = ProjectData.create_project_data_with_invalid_ids(ids)
    yield project


@pytest.fixture
def project_data_with_invalid_name(super_admin):
    project = ProjectData.create_project_data_with_invalid_name
    yield project


@pytest.fixture(params=["Root", " Root", "_Root4", "_Root "])
def project_data_with_invalid_parentProject(request, super_admin):
    variant = request.param
    project = ProjectData.create_project_data_with_invalid_parentProject(variant)
    yield project


@pytest.fixture
def project_data_with_empty_parentProject(super_admin):
    project = ProjectData.create_project_data_with_empty_parentProject
    yield project


@pytest.fixture
def project_data_with_false(super_admin):
    project_id_pool = []
    def _create_project_data_with_false():
        project = ProjectData.create_project_data_with_false()
        project_id_pool.append(project.id)
        return project

    yield _create_project_data_with_false

    for project_id in project_id_pool:
        super_admin.api_manager.project_api.clean_up_project(project_id)


@pytest.fixture(params=[DataGenerator.fake_build_id()])
def build_conf_data(super_admin, project_data, request):
    build_id_pool = []

    def _create_build_conf_data():
        name = request.param
        build_conf = BuildConfData.create_build_conf_data(project_data.id, name)
        build_id_pool.append(build_conf.id)
        return build_conf

    yield _create_build_conf_data()

    for build_conf_id in build_id_pool:
        super_admin.api_manager.build_conf_api.clean_up_build(build_conf_id)


@pytest.fixture(params=[DataGenerator.fake_build_id()])
def build_conf_data_without_deleting_id(super_admin, project_data, request):
        name = request.param
        build_conf = BuildConfData.create_build_conf_data(project_data.id, name)
        yield build_conf


@pytest.fixture
def build_conf_data_with_empty_steps_field(super_admin, project_data):
    build_id_pool = []

    def _create_build_conf_data():
        build_conf = BuildConfData.create_build_conf_data_with_empty_steps(project_data.id)
        build_id_pool.append(build_conf.id)
        return build_conf

    yield _create_build_conf_data

    for build_conf_id in build_id_pool:
        super_admin.api_manager.build_conf_api.clean_up_build(build_conf_id)


@pytest.fixture
def build_conf_data_copy(super_admin, build_conf_data):
    build_id_pool = []

    def _create_build_conf_data():
        build_conf = BuildConfData.create_build_conf_data_copy(build_conf_data.id)
        build_id_pool.append(build_conf.id)
        return build_conf

    yield _create_build_conf_data()

    for build_conf_id in build_id_pool:
        super_admin.api_manager.build_conf_api.clean_up_build(build_conf_id)


@pytest.fixture
def build_conf_data_copy_with_invalid_parent_build_conf(super_admin):
        build_conf = BuildConfData.create_build_conf_data_copy_with_invalid_parent_build_conf()
        yield build_conf


@pytest.fixture
def build_conf_data_without_steps_field(super_admin, project_data):
    build_id_pool = []

    def _create_build_conf_data():
        build_conf = BuildConfData.create_build_conf_data_without_steps(project_data.id)
        build_id_pool.append(build_conf.id)
        return build_conf

    yield _create_build_conf_data

    for build_conf_id in build_id_pool:
        super_admin.api_manager.build_conf_api.clean_up_build(build_conf_id)


@pytest.fixture
def build_conf_data_with_empty_id(super_admin, project_data):
        build_conf = BuildConfData.create_build_conf_data_with_empty_id(project_data.id)
        yield build_conf


@pytest.fixture
def build_conf_data_with_empty_name(super_admin, project_data):
    build_conf = BuildConfData.create_build_conf_data_with_empty_name(project_data.id)
    yield build_conf


@pytest.fixture(params=["", DataGenerator.incorrect_id_1(), DataGenerator.fake_project_id()])
def build_conf_data_with_invalid_project_id(request, super_admin):
    project_ids = request.param
    build_conf = BuildConfData.create_build_conf_data_with_invalid_project_id(project_ids)
    yield build_conf


@pytest.fixture(params=[DataGenerator.incorrect_id_1(), DataGenerator.incorrect_id_2(),DataGenerator.incorrect_id_3()])
def build_data_with_invalid_ids(request, super_admin, project_data):
    ids = request.param
    build_conf = BuildConfData.create_build_conf_data_with_invalid_ids(project_data.id, ids)
    yield build_conf


@pytest.fixture
def build_conf_run_data(super_admin, build_conf_data):
        build_conf_run = BuildRunData.create_run_build_correct_data(build_conf_data.id)
        yield build_conf_run


@pytest.fixture
def build_conf_run_data_with_wrong_build_conf_id(super_admin):
    build_conf_run = BuildRunData.create_run_build_incorrect_data()
    yield build_conf_run


@pytest.fixture
def build_conf_run_cancel(super_admin):
    build_conf_run_cancel = BuildRunData.cancel_build_conf_in_queue()
    yield build_conf_run_cancel


