from typing import Optional, Dict
from utilis.data_generator import DataGenerator
from pydantic import BaseModel

#Начало описание модели для запуска билда (запрос)
class BuildTypeRunModel(BaseModel):
    id: str
    name: str
    projectName: str
    projectId: str
    href: str
    webUrl: str


class UserModel(BaseModel):
    username: str
    id: int
    href: str


class TriggeredModel(BaseModel):
    type: str
    date: str
    user: UserModel


class BuildTypesModel(BaseModel):
    id: str


class BuildRunRequestModel(BaseModel):
    buildType: BuildTypesModel

    class Config:
        extra = "allow"


class BuildRunCancelRequestModel(BaseModel):
    comment: str
    readdIntoQueue: bool


#Конец описание модели для запуска билда (запрос)

#Начало описание модели запуска билда (ответ)
class BuildRunResponseModel(BaseModel):
    id: int
    buildTypeId: str
    state: str
    href: str
    webUrl: str
    buildType: BuildTypeRunModel
    waitReason: str
    queuedDate: str
    triggered: TriggeredModel
    changes: Optional[dict]
    revisions: Optional[dict]
    compatibleAgents: Optional[dict]
    artifacts: Optional[dict]
    vcsLabels: Optional[list]
    customization: Optional[dict] = None

    class Config:
        extra = "allow"


class BuildRunCancelResponseModel(BaseModel):
    id: int
    buildTypeId: str
    number: str
    status: str
    state: str
    href: str
    webUr: Optional[str] = None
    statusText: str
    buildType: BuildTypeRunModel
    canceledInfo: dict
    queuedDate: str
    startDate: str
    finishDate: str
    triggered: dict
    changes: dict
    revisions: Dict[str, int]
    agent: dict
    artifacts: dict
    relatedIssues: dict
    statistics: dict
    vcsLabels: list = []
    finishOnAgentDate: str
    customization: dict = None

#Конец описание модели запуска билда (ответ)

class BuildConfRunStatusModel(BaseModel):
    count: int
    href: str
    build: list

class BuildRunData:

    @staticmethod
    def create_run_build_correct_data(build_conf_id) -> BuildRunRequestModel:
        return (BuildRunRequestModel(
            buildType = {"id": build_conf_id}
        ))

    @staticmethod
    def create_run_build_incorrect_data() -> BuildRunRequestModel:
        return (BuildRunRequestModel(
            buildType = {"id": DataGenerator.fake_build_id()}
        ))

    @staticmethod
    def create_run_build_data_with_invalid_id() -> BuildRunRequestModel:
        return (BuildRunRequestModel(
            buildType = {"id": DataGenerator.fake_build_id()}
        ))

    @staticmethod
    def create_run_build_data_with_empty_dict() -> BuildRunRequestModel:
        return (BuildRunRequestModel(
            buildType = {}
        ))

    @staticmethod
    def cancel_build_conf_in_queue() -> BuildRunCancelRequestModel:
        return (BuildRunCancelRequestModel(
            comment="Canceling a queued build",
            readdIntoQueue=False
        ))






