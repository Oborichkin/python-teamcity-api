from .api.server import Server

s = Server()
print(s.version)
# print(s.projects[1].buildTypes[0].builds[0].artifacts.files[0].download())
# print(s.projects[2].subprojects[0].buildTypes[0].builds[0].artifacts.files)
