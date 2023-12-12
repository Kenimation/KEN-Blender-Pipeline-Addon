import os
import bpy
import bpy.utils.previews

class icons():
    def __init__(self, filepath):
        self.pcoll = bpy.utils.previews.new()
        fileloc = os.path.join(os.path.dirname(__file__), filepath)
        self.fileloc = fileloc = os.path.normpath(fileloc)

    def getColl(self): 
        return self.pcoll

    def load(self, coll):
        fileNames = os.listdir(self.fileloc)
        for fileName in fileNames:
            namesplit = str(fileName).split('.')
            coll.load(str(namesplit[0]), os.path.join(self.fileloc, str(fileName)), 'IMAGE')