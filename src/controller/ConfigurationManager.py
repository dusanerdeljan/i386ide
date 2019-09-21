class ConfigurationManager(object):

    def __init__(self):
        self.currentProject = None
        self.allProjects = list()

    def setCurrentProject(self, project):
        self.currentProject = project
