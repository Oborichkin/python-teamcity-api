from ..import get
from .project import Project


class Server:
    PATH = "server"

    @property
    def version(self):
        return get(path="server")["version"]

    @property
    def projects(self):
        return Project.many_from_list(get(path="projects")["project"])

    @property
    def vscRoots(self):
        # TODO
        pass

    @property
    def builds(self):
        # TODO
        pass

    @property
    def users(self):
        # TODO
        pass

    @property
    def userGroups(self):
        # TODO
        pass

    @property
    def agents(self):
        # TODO
        pass

    @property
    def buildQueue(self):
        # TODO
        pass

    @property
    def agentPools(self):
        # TODO
        pass

    @property
    def investigations(self):
        # TODO
        pass

    @property
    def mutes(self):
        # TODO
        pass
