class Document:
    def __init__(self, name, date, driverName):
        self.name = name
        self.date = date
        self.driverName = driverName

class Driver:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.documents = []

    def addDocument(self, document):
        self.documents.extend(document)