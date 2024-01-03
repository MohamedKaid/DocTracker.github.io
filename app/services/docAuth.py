import datetime as date1
from dateutil import parser
from services.DataService import *
from database.Dbase import *

"""
    Expiration dates calculated
"""
# class inputDocumnet:
        
   
#requests all docs for a spicific email from the database
#sends the list to the creatHash function to return it in a hash map format 
#check date if less than a four week time spam if so sends the appropriate message
def getExpiredDocuments(email):
    # Today's date
    today= date1.datetime.today()

    # All documents for current dispatcher
    documents = DataService.docData(email)
    
    # Calculate documents expiring within 28 days
    soonToExpireDocuments = []
    for document in documents:
        # Convert to date format
        expiration_date = datetime.strptime(document.date, '%m-%d-%Y')
        fourWeekRange = expiration_date - today
        
        if 0 <= fourWeekRange.days < 28:
            soonToExpireDocuments.append(document)

    return soonToExpireDocuments

# if __name__ == "__main__":
#     driverObj = inputDocumnet()
#     driverObj.checkDocExp("am@gmail.com")