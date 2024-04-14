from typing import Optional, Dict
from utilis.data_generator import DataGenerator
from pydantic import BaseModel


class ProjectModule(BaseModel):
    id: str
    name: str
    parentProjectId: str
    href: str
    webUrl: str


class Templates(BaseModel):
    count: int
    buildType: list = []


class PropertyModel(BaseModel):
    name: str
    value: str


class ParametersModel(BaseModel):
    property: list = []
    count: int
    href: str


class FeaturesModel(BaseModel):
    count: int


class TriggersModel(BaseModel):
    count: int


class BuildsModel(BaseModel):
    href: str


class InvestigationsModel(BaseModel):
    href: str


class CompatibleAgentsModel(BaseModel):
    href: str


class BuildResponseModel(BaseModel):

    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str
    project: ProjectModule
    templates: Optional[Templates] = None
    settings: Optional[dict]
    parameters: Optional[ParametersModel] = None
    steps: Optional[dict] = None
    features: Optional[FeaturesModel] = None
    triggers: Optional[TriggersModel] = None
    builds: Optional[BuildsModel] = None
    investigations: Optional[InvestigationsModel] = None
    compatibleAgents: Optional[CompatibleAgentsModel] = None

    class Config:
        extra = "allow"


class BuildDataModel(BaseModel):
    id: str
    name: str
    project: Dict[str, str]
    steps: Optional[dict] = None

    class Config:
        extra = "allow"


class BuildDataCopyModel(BaseModel):
    sourceBuildTypeLocator: str
    name: str
    id: str
    copyAllAssociatedSettings: bool


class BuildConfData:
    @staticmethod
    def build_conf_data(project_id, name) -> BuildDataModel:
        # Метод по генерации данных для билда
        return (BuildDataModel(
            id=DataGenerator.fake_build_id(),
            name=name,
            project={"id": project_id},
            steps={"step": [
                    {
                        "name": "myCommandLineStep",
                        "type": "simpleRunner",
                        "properties": {
                            "property": [
                                {
                                    "name": "script.content",
                                    "value": "echo 'Hello World!'"
                                },
                                {
                                    "name": "teamcity.step.mode",
                                    "value": "default"
                                },
                                {
                                    "name": "use.custom.script",
                                    "value": "true"
                                }
                            ]
                        }
                    }
                ]}))

    @staticmethod
    def build_data_empty_steps(project_id) -> BuildDataModel:
        return (BuildDataModel(
            id=DataGenerator.fake_build_id(),
            name=DataGenerator.fake_name(),
            project={"id": project_id},
            steps={}
        ))

    @staticmethod
    def build_data_without_steps(project_id) -> BuildDataModel:
        return (BuildDataModel(
            id=DataGenerator.fake_build_id(),
            name=DataGenerator.fake_name(),
            project={"id": project_id},
        ))

    @staticmethod
    def build_data_empty_id(project_id) -> BuildDataModel:
        return (BuildDataModel(
            id="",
            name=DataGenerator.fake_name(),
            project={"id": project_id},
            steps={"step": [
                {
                    "name": "myCommandLineStep",
                    "type": "simpleRunner",
                    "properties": {
                        "property": [
                            {
                                "name": "script.content",
                                "value": "echo 'Hello World!'"
                            },
                            {
                                "name": "teamcity.step.mode",
                                "value": "default"
                            },
                            {
                                "name": "use.custom.script",
                                "value": "true"
                            }
                        ]
                    }
                }
            ]}))

    @staticmethod
    def build_data_empty_name(project_id) -> BuildDataModel:
        return (BuildDataModel(
            id=DataGenerator.fake_build_id(),
            name="",
            project={"id": project_id},
            steps={"step": [
                {
                    "name": "myCommandLineStep",
                    "type": "simpleRunner",
                    "properties": {
                        "property": [
                            {
                                "name": "script.content",
                                "value": "echo 'Hello World!'"
                            },
                            {
                                "name": "teamcity.step.mode",
                                "value": "default"
                            },
                            {
                                "name": "use.custom.script",
                                "value": "true"
                            }
                        ]
                    }
                }
            ]}))

    @staticmethod
    def build_data_invalid_project_id(project_ids) -> BuildDataModel:
        return (BuildDataModel(
            id=DataGenerator.fake_build_id(),
            name=DataGenerator.fake_name(),
            project={"id": project_ids},
            steps={"step": [
                {
                    "name": "myCommandLineStep",
                    "type": "simpleRunner",
                    "properties": {
                        "property": [
                            {
                                "name": "script.content",
                                "value": "echo 'Hello World!'"
                            },
                            {
                                "name": "teamcity.step.mode",
                                "value": "default"
                            },
                            {
                                "name": "use.custom.script",
                                "value": "true"
                            }
                        ]
                    }
                }
            ]}))

    @staticmethod
    def build_data_invalid_ids(project_id, ids) -> BuildDataModel:
        return (BuildDataModel(
            id=ids,
            name=DataGenerator.fake_name(),
            project={"id": project_id},
            steps={"step": [
                {
                    "name": "myCommandLineStep",
                    "type": "simpleRunner",
                    "properties": {
                        "property": [
                            {
                                "name": "script.content",
                                "value": "echo 'Hello World!'"
                            },
                            {
                                "name": "teamcity.step.mode",
                                "value": "default"
                            },
                            {
                                "name": "use.custom.script",
                                "value": "true"
                            }
                        ]
                    }
                }
            ]}))

    @staticmethod
    def build_data_copy(build_conf_id) -> BuildDataCopyModel:
        return (BuildDataCopyModel(
            sourceBuildTypeLocator=build_conf_id,
            name=DataGenerator.fake_name(),
            id=DataGenerator.fake_build_id(),
            copyAllAssociatedSettings=True
        ))

    @staticmethod
    def build_invalid_parent() -> BuildDataCopyModel:
        return (BuildDataCopyModel(
            sourceBuildTypeLocator=DataGenerator.fake_build_id(),
            name=DataGenerator.fake_name(),
            id=DataGenerator.fake_build_id(),
            copyAllAssociatedSettings=True
        ))
