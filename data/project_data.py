from typing import Optional, Dict
from utilis.data_generator import DataGenerator
from pydantic import BaseModel


class Templates(BaseModel):
    count: int
    buildType: list = []


class ParametersModel(BaseModel):
    property: list = []
    count: int
    href: str


class ParentProjectModel(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    href: str
    webUrl: str


class BuildTypes(BaseModel):
    count: int
    buildType: list = []


class VcsRoots(BaseModel):
    count: int
    href: str


class ProjectFeatures(BaseModel):
    count: int
    href: str


class ProjectResponseModel(BaseModel):
    id: str
    name: str
    parentProjectId: str
    virtual: bool
    href: str
    webUrl: str
    parentProject: ParentProjectModel
    buildTypes: Optional[BuildTypes] = None
    templates: Optional[Templates] = None
    deploymentDashboards: Optional[dict[str, int]] = None
    parameters: Optional[ParametersModel] = None
    vcsRoots: Optional[VcsRoots] = None
    projectFeatures: Optional[ProjectFeatures] = None
    projects: dict

    class Config:
        extra = "allow"


class ProjectDataModel(BaseModel):
    parentProject: Dict[str, str]
    name:  str
    id: str
    copeAllAssociatedSettings: bool


class ProjectDataCopyModel(BaseModel):
    parentProject: Dict[str, str]
    name:  str
    id: str
    copeAllAssociatedSettings: bool
    sourceProject: Dict[str, str]


class ProjectData:
    @staticmethod
    def create_project_data_with_correct_data(name) -> ProjectDataModel:
        # Метод, генерирующий данные проекта, использую уникальные значения name и id
        return (ProjectDataModel(
            parentProject={"locator": "_Root"},
            name=name,
            id=DataGenerator.fake_project_id(),
            copeAllAssociatedSettings=True
        ))

    @staticmethod
    def create_first_project_data_with_correct_data() -> ProjectDataModel:
        # Метод, генерирующий данные проекта, использую уникальные значения name и id
        return (ProjectDataModel(
            parentProject={"locator": "_Root"},
            name=DataGenerator.fake_build_id(),
            id=DataGenerator.fake_build_id(),
            copeAllAssociatedSettings=True
        ))

    @staticmethod
    def create_project_data_with_data() -> ProjectDataModel:
        return (ProjectDataModel(
            parentProject={"locator": "_Root"},
            name=DataGenerator.fake_name(),
            id=DataGenerator.fake_project_id(),
            copeAllAssociatedSettings=True
        ))

    @staticmethod
    def create_project_data_copy(project_id) -> ProjectDataCopyModel:
        return (ProjectDataCopyModel(
            parentProject={"locator": "_Root"},
            name=DataGenerator.fake_name(),
            id= DataGenerator.fake_project_id(),
            copeAllAssociatedSettings=True,
            sourceProject={"locator": project_id}

        ))

    @staticmethod
    def create_project_data_copy_with_another_source_project() -> ProjectDataCopyModel:
        return (ProjectDataCopyModel(
            parentProject={"locator": "_Root"},
            name=DataGenerator.fake_name(),
            id=DataGenerator.fake_project_id(),
            copeAllAssociatedSettings=True,
            sourceProject={"locator": DataGenerator.fake_build_id()}

        ))

    @staticmethod
    def create_project_data_with_empty_parentProject() -> ProjectDataModel:
        return (ProjectDataModel(
            parentProject={"locator": ""},
            name=DataGenerator.fake_name(),
            id=DataGenerator.fake_project_id(),
            copeAllAssociatedSettings=True
        ))

    @staticmethod
    def create_project_data_with_invalid_parentProject(variant) -> ProjectDataModel:
        return (ProjectDataModel(
            parentProject={"locator": variant},
            name=DataGenerator.fake_name(),
            id=DataGenerator.fake_project_id(),
            copeAllAssociatedSettings=True
        ))

    @staticmethod
    def create_project_data_with_invalid_name() -> ProjectDataModel:
        return (ProjectDataModel(
            parentProject={"locator": "_Root"},
            name="",
            id=DataGenerator.fake_project_id(),
            copeAllAssociatedSettings=True
        ))

    @staticmethod
    def create_project_data_with_empty_id() -> ProjectDataModel:
        return (ProjectDataModel(
            parentProject={"locator": "_Root"},
            name=DataGenerator.fake_name(),
            id="",
            copeAllAssociatedSettings = True
        ))

    @staticmethod
    def create_project_data_with_invalid_ids(ids) -> ProjectDataModel:
        return (ProjectDataModel(
            parentProject={"locator": "_Root"},
            name=DataGenerator.fake_name(),
            id=ids,
            copeAllAssociatedSettings=True
        ))

    @staticmethod
    def create_project_data_with_false() -> ProjectDataModel:
        return (ProjectDataModel(
            parentProject={"locator": "_Root"},
            name=DataGenerator.fake_name(),
            id=DataGenerator.fake_project_id(),
            copeAllAssociatedSettings=False
        ))














