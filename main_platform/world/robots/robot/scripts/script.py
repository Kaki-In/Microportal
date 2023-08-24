class Script():
    def __init__(self, user):
        self._title = "New Script"
        self._name = ""
        self._args = {}
        self._user = user
    
    def setName(self, name):
        self._name = name
    
    def name(self):
        return self._name
    
    def title(self):
        return self._title
    
    def setTitle(self, title):
        self._title = title
    
    def user(self):
        return self._user
    
    def __getitem__(self, key):
        return self._args[ key ]
    
    def __setitem__(self, key, value):
        self._args[ key ] = value
    
    def arguments(self):
        return self._args.copy()
    
    def __iter__(self):
        return iter(self._args)
    
    def __len__(self):
        return len(self._args)
    
    def toJson(self):
        return {
                   "name": self._name,
                   "args": self._args,
                   "user": self._user,
                   "title": self._title,
               }
    
    def fromJson(json):
        s = Script()
        s._name = json[ 'name' ]
        s._args = json[ 'args' ]
        s._user = json[ 'user' ]
        s._title = json[ 'title' ]
