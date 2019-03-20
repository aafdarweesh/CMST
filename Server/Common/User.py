class User:
    def __init__(self, ID):
        self.Name = ""
        self.Surname = ""
        self.ID = ID

    #set the name of the user
    def setName(self, name):
        self.Name = name

    #set the surname of the user
    def setSurname(self, surname):
        self.Surname = surname

    #get the ID of the user
    def getID(self):
        return self.ID

    #get the Name of the user
    def getName(self):
        return self.Name

    #get the Surname of the user
    def getSurname(self):
        return self.Surname
