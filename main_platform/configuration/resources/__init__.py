import os as _os

class ResourcesDirectory():
    def __init__(self, directory, files):
        self._directory = directory
        self._files = files

        if not _os.path.exists(directory):
            _os.makedirs(directory)

        for file in files:
            path = directory + "/" + file
            if _os.path.exists(path):
                a = open(path, "r")
                files[ file ] = a.read()
                a.close()
            else:
                a = open(path, "w")
                a.write(files[ file ])
                a.close()
		
    def getFile(self, filename):
         if filename in self._files:
             return self._files[ filename ]
         else:
             raise FileNotFoundError("no such resource")

