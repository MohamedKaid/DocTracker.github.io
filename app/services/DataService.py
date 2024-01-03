from datetime import datetime
from database.Dbase import *
from database.Entities import *

class DataService:
    
    @staticmethod
    def driverData(email):
        # TODO: remove requiring Dbase instance
        # Database instance
        db = Dbase()
        
        # Get dispatch id and retrieve drivers
        dispatch_id = db.getDispatchId(email)
        drivers_records = Dbase.getData(dispatch_id)
        
        # Create driver object for each driver
        drivers = [Driver(*record) for record in drivers_records]

        # Sort drivers
        drivers = sorted(drivers, key=lambda x: x.name)

        for driver in drivers:
            # Retrieve documents
            doc_records = Dbase.getDoc(driver.id)

            # Create document object for each document
            documents = [Document(*record) for record in doc_records]

            # Sort documents by date
            documents = sorted(documents, key=lambda x: datetime.strptime(x.date, '%m-%d-%Y'))

            # Add documents to driver object
            driver.addDocument(documents)
    
        return drivers
    
    @staticmethod
    def docData(email):
        db = Dbase()

        # Get all document records
        doc_records = db.getAllDocs(email)

        # Create document object for each document
        documents = [Document(*record) for record in doc_records]

        # Sort documents by date
        documents = sorted(documents, key=lambda x: datetime.strptime(x.date, '%m-%d-%Y'))
        
        return documents
    