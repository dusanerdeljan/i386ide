class ConfigurationManager(object):

    def __init__(self):
        self.currentProject = None
        self.allProjects = []

    def setCurrentProject(self, project):
        self.currentProject = project
