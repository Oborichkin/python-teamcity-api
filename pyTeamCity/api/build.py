import os
from urllib.parse import urlparse

from .. import get
from .base import Base


class BuildType(Base):
    def __init__(self):
        super().__init__()
        self.paused = False
        self.projectName = None
        self.description = None
        self.projectId = None

    @property
    def builds(self):
        return Build.many_from_list(get(href=f"{self.href}/builds/")["build"])

    @property
    def investigations(self):
        pass

    @property
    def compatibleAgents(self):
        pass


class Build(Base):
    def __init__(self):
        super().__init__()
        self.buildTypeId = None
        self.number = None
        self.status = None
        self.state = None
        self.branchName = None
        self.defaultBranch = None

    @property
    def statusText(self):
        return get(href=self.href)["statusText"]

    @property
    def buildType(self):
        return BuildType.from_obj(get(href=self.href)["buildType"])

    @property
    def artifacts(self):
        return Artifacts.from_files_list(get(href=f"{self.href}/artifacts/children")["file"])

    def __repr__(self):
        return f"<Build({self.id}): #{self.number}>"


class Artifacts:
    def __init__(self):
        self.files = []

    @staticmethod
    def from_files_list(lst):
        a = Artifacts()
        a.files = [File.from_obj(f) for f in lst]
        return a


class File(Base):
    def __init__(self):
        super().__init__()
        self.name = None
        self.size = None
        self.modificationTime = None
        self.href = None
        self.content = None

    def __repr__(self):
        return self.name

    def download(self, output=None):
        url = self.content["href"]
        output = output if output else os.path.basename(urlparse(url).path)
        r = get(href=url, to_json=False)
        with open(output, 'wb') as f:
            f.write(r.content)
