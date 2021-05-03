import requests
import os
import urllib.request
from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth

HOST = os.environ.get("TEAMCITY_HOST")
USER = os.environ.get("TEAMCITY_USER")
PWD = os.environ.get("TEAMCITY_PWD")

auth = HTTPBasicAuth(USER, PWD)


def get(path=None, href=None, to_json=True):
    assert path or href
    if path:
        r = requests.get(f"{HOST}/app/rest/{path}", auth=auth, headers={"accept": "application/json"})
    else:
        r = requests.get(f"{HOST}{href}", auth=auth, headers={"accept": "application/json"})
    return r.json() if to_json else r


class Base:
    def __init__(self):
        self.id = None
        self.name = None
        self.href = None
        self.webUrl = None

    @classmethod
    def from_obj(cls, obj):
        c = cls()
        for key, value in obj.items():
            setattr(c, key, value)
        return c

    @classmethod
    def many_from_list(cls, lst):
        return [cls.from_obj(c) for c in lst]

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id}): {self.name}>"


class Server:
    @property
    def projects(self):
        return Project.many_from_list(get(path="projects")["project"])


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


class BuildType(Base):
    def __init__(self):
        super().__init__()
        self.paused = False
        self.projectName = None
        self.description = None
        self.projectId = None

    @property
    def project(self):
        return Project.from_obj(get(href=self.href)["project"])

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


if __name__ == "__main__":
    s = Server()
    print(s.projects[1].buildTypes[0].builds[0].artifacts.files[0].download())
    # print(s.projects[2].subprojects[0].buildTypes[0].builds[0].artifacts.files)
