from .. import get
from .base import Base
from .build import BuildType


class Project(Base):
    def __init__(self):
        super().__init__()
        self.archived = False
        self.description = None
        self.parentProjectId = None

    @property
    def parentProject(self):
        if self.parentProjectId:
            return Project.from_obj(get(href=self.href)["parentProject"])

    @property
    def subprojects(self):
        return Project.many_from_list(get(href=self.href)["projects"]["project"])

    @property
    def buildTypes(self):
        return BuildType.many_from_list(get(href=self.href)["buildTypes"]["buildType"])
