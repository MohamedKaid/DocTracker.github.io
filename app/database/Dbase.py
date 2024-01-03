import sqlite3
import os
from datetime import date

class Dbase():
    
    # Establish the connection to the database
    @staticmethod
    def connect():
        conn = sqlite3.connect("app/database/docTracker.db")
        cursor = conn.cursor()

        return conn, cursor
    
    # Close the connection to the database
    @staticmethod
    def disconnect(conn, cursor):
        cursor.close()
        conn.close()



    # Reads and creates a db using a .sql file
    def setUpDB(Dbase):
        db_file = "docTracker.db"
        
        if not os.path.exists(db_file):
            # connect to or make new sqlite DB 
            conn, cursor = Dbase.connect()
            
            # read the .sql file into sql_script
            with open ("DB\\create_DB_tables.sql") as file:
                sql_script = file.read()
            
            # execute the script
            cursor.executescript(sql_script)
            
            # close the cursor and the connection
            Dbase.disconnect(conn, cursor)
        else:
            print("DB already exists")
    
    
    # Displays the DB tables and all the attributes
    @staticmethod
    def displayDB():
        # Connect to your SQLite database
        conn, cursor = Dbase.connect()

        # Get the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # For each table, retrieve its attributes
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name});")
            table_info = cursor.fetchall()

            # Print the table name and its attributes
            print(f"Table: {table_name}")
            for info in table_info:
                print(f"Column Name: {info[1]}, Data Type: {info[2]}")

        # Close the cursor and the connection
        Dbase.disconnect(conn, cursor)
    
    
    # Delete the Data Base
    @staticmethod
    def deleteDB():
        # Specify the path to your SQLite database file
        db_file = "docTracker.db"

        # Check if the database file exists
        if os.path.exists(db_file):
            # Delete the database file
            os.remove(db_file)
            print(f"Database '{db_file}' has been deleted.")
        else:
            print(f"Database '{db_file}' does not exist.")
    
    
    # Add a dispatcher to the dispatch Table
    @staticmethod
    def addDispatcher(email,pin):
        # Connection/cursor
        conn, cursor = Dbase.connect()

        # Sql statement
        insert_query = f"INSERT INTO Dispatch (email, pin) VALUES (?,?)"

        # Execute insert and commit
        try:
            cursor.execute(insert_query,(email, pin))
            conn.commit()

        # Catch exception thrown if value already exists
        except sqlite3.IntegrityError as e:
            # Pass the exception to the calling function
            raise sqlite3.IntegrityError
        
        # Close the cursor and the connection
        finally:
            Dbase.disconnect(conn, cursor)
  
  
    # Display all data in a table
    @staticmethod
    def displayTable(table_name):
        # Connect to your SQLite database
        conn, cursor = Dbase.connect()

        # Define the SQL insert statement
        insert_query = f"Select * from {table_name}"

        # Execute the insert statement
        cursor.execute(insert_query)
        
        #fetching all the records
        records = cursor.fetchall()
        
        #displaying the records
        for records in records:
            print(records)
         
        # Commit the changes to the database
        conn.commit()

        # Close the cursor and the connection
        Dbase.disconnect(conn, cursor)
    
    
    # Delete a record or row from the dispatch Table  
    @staticmethod 
    def deleteDispatchRec(name):
        conn, cursor = Dbase.connect()
        
        sql = f"DELETE from Dispatch WHERE name = ?;"
        
        cursor.execute(sql, (name,))
        conn.commit()
        
        Dbase.disconnect(conn, cursor)
    
    
    # Get the dispatcher Id to be used when adding the driver
    @staticmethod
    def getDispatchId(email):
        conn, cursor = Dbase.connect()
        
        # Get a dispatch ID 
        sql = "SELECT dispatch_id FROM Dispatch Where email = ?;"

        cursor.execute(sql, (email,))
        
        dispatch_id = cursor.fetchone()
        
        Dbase.disconnect(conn, cursor)
        
        if dispatch_id is not None:
            return dispatch_id[0]  # Access the first element of the tuple (dispatch_id)
        else:
            return None
        
        
    # Add a driver to the driver table 
    @staticmethod
    def addDriver(driver_name, dispatch_email):
        
        dispatch_id = Dbase.getDispatchId(dispatch_email)
        if dispatch_id is not None:  
            # Connect to your SQLite database
            conn, cursor = Dbase.connect()
            
            # Define the SQL insert statement
            insert_query = "INSERT INTO drivers (name, dispatch_id) VALUES (?, ?);"

            # Specify the values to insert
            value = (driver_name, dispatch_id)

            # Execute the insert statement
            try:
                cursor.execute(insert_query, (value))
                # Commit the changes to the database
                conn.commit()

                # Return new driver id
                return Dbase.getDriverId(driver_name)

            # Catch exception thrown if value already exists
            except sqlite3.IntegrityError as e:
                # Pass the exception to the calling function
                raise sqlite3.IntegrityError
            
            # Close the cursor and the connection
            finally:
                Dbase.disconnect(conn, cursor)
        else:
            print(f"Dispatch ID is NONE: {dispatch_id}")
        
     
    # Get the driver id from the Drivers table       
    @staticmethod
    def getDriverId(name):
        # Connection
        conn, cursor = Dbase.connect()
        
        # Get a driver_id ID 
        sql = "SELECT driver_id FROM Drivers Where name = ?;"

        cursor.execute(sql, (name,))
        
        driver_id = cursor.fetchone()
        
        Dbase.disconnect(conn, cursor)
        
        if driver_id is not None:
            return driver_id[0]  # Access the first element of the tuple (driver_id)
        else:
            return None
    
    
    @staticmethod
    def deleteDriver(driver_id):
        conn, cursor = Dbase.connect()
        
        sql = f"DELETE from Drivers WHERE driver_id = ?;"
        
        doc_sql = f"DELETE FROM DriverDocs WHERE driver_id =?"
        cursor.execute(sql, (driver_id,))
        cursor.execute(doc_sql, (driver_id,))
        conn.commit()
        
        Dbase.disconnect(conn, cursor)
    
    # Add a driver Document to the DriverDocs table
    @staticmethod 
    def addDcoument(doc_name, exp_date, driverId):

        if driverId is not None:  
            # Connect to your SQLite database
            conn, cursor = Dbase.connect()
            
            # Define the SQL insert statement
            insert_query = "INSERT INTO DriverDocs (doc_name, exp_date, driver_id) VALUES (?, ?, ?);"

            # Specify the values to insert
            value = (doc_name, exp_date, driverId)

            # Execute the insert statement
            cursor.execute(insert_query, (value))

            # Commit the changes to the database
            conn.commit()

            # Close the cursor and the connection
            Dbase.disconnect(conn, cursor)
        else:
            print(f"Driver ID is NONE: {driverId}")
            
    @staticmethod
    def getDoc(driver_id):
        # driver_id = Dbase.getDriverId(driver_name)
        conn, cursor = Dbase.connect()
        
        sql = "SELECT * FROM DriverDocs WHERE driver_id = ?;"
        
        cursor.execute(sql, (driver_id,))
        
        records = cursor.fetchall()

        Dbase.disconnect(conn, cursor)

        return records
    
    # Returns doc name, exp_date, driver name
    @staticmethod
    def getAllDocs(email):
        conn, cursor = Dbase.connect()

        dispatchId = Dbase.getDispatchId(email)

        sql = '''
                SELECT DriverDocs.doc_name, DriverDocs.exp_date, Drivers.name 
                FROM DriverDocs 
                JOIN Drivers ON DriverDocs.driver_id = Drivers.driver_id 
                WHERE Drivers.dispatch_id = ?
        '''
        cursor.execute(sql, (dispatchId,))
        documents = cursor.fetchall()

        Dbase.disconnect(conn, cursor)

        return documents


    def getAllDispatchers():
        conn, cursor = Dbase.connect()

        sql = 'SELECT email FROM dispatch'
        cursor.execute(sql)

        # Get first value in tuple for each record
        emails = [row[0] for row in cursor.fetchall()]

        Dbase.disconnect(conn, cursor)

        return emails
    
            
    @staticmethod
    def logIn(email):
        conn, cursor = Dbase.connect()
        
        sql = "SELECT pin FROM Dispatch WHERE email = ?"
        
        cursor.execute(sql, (email,))
        
        pin = cursor.fetchone()
        
        Dbase.disconnect(conn, cursor)
        
        if pin is not None:
            return pin[0]
        else:
            return None
        
    @staticmethod
    def getData(dispatch_id):
        conn, cursor = Dbase.connect()

        query = "Select Driver_id, name from Drivers where dispatch_id = ?;"
        cursor.execute(query, (dispatch_id,))

        records = cursor.fetchall()

        Dbase.disconnect(conn, cursor)

        return records


    # Display all data in a table
    @staticmethod
    def getDrivers(table_name, dispatch_email):
        # Connect to your SQLite database
        conn, cursor = Dbase.connect()

        # Define the SQL insert statement
        query = f"Select driver_id, name from {table_name} WHERE dispatch_id = ?;"

        dispatch_id = Dbase.getDispatchId(dispatch_email)

        # Execute the insert statement
        cursor.execute(query, (dispatch_id,))
        
        #fetching all the records
        records = cursor.fetchall()
         
        # Commit the changes to the database
        conn.commit()

        # Close the cursor and the connection
        Dbase.disconnect(conn, cursor)

        return records
    
    @staticmethod
    def deleteDoc(doc_name, doc_date, driver_id):
        conn, cursor = Dbase.connect()
        
        sql= f"DELETE from DriverDocs Where doc_name = ? AND exp_date=? And driver_id=?"
        
        cursor.execute(sql, (doc_name, doc_date, driver_id, ))
        
        conn.commit()
        
        Dbase.disconnect(conn, cursor)

    # Update records in the table

    @staticmethod
    def changeEmail(email, pin, newEmail):
        if(Dbase.isValidPassword(email, pin)):
            conn, cursor = Dbase.connect()
            checkEmail = "SELECT email FROM Dispatch WHERE email = ?"
        
            cursor.execute(checkEmail,(email, ))
            record = cursor.fetchone()
            
            if record == None or email != record[0]:
                return "Wrong email input"
            else:
                sql = "UPDATE Dispatch SET email = ? WHERE email = ?"
                cursor.execute(sql, (newEmail, email))
                conn.commit()
            
            Dbase.disconnect(conn, cursor)
        else:
            raise Exception

    
    @staticmethod
    def changePass(email, oldPin, newPin):
        if(Dbase.isValidPassword(email, oldPin)):
            conn, cursor = Dbase.connect()

            sql = f"UPDATE Dispatch SET pin = ? WHERE email = ? "
            cursor.execute(sql, (newPin, email,  ))
            conn.commit()

            Dbase.disconnect(conn, cursor)
        else:
            raise Exception
        

    @staticmethod
    def isValidPassword(email, givenPassword):
        conn, cursor = Dbase.connect()

        # Get password
        sql = 'SELECT pin FROM Dispatch WHERE email = ?'

        cursor.execute(sql, (email,))
        conn.commit()
        resultPassword = cursor.fetchone()

        Dbase.disconnect(conn, cursor)
        
        # Return boolean
        return resultPassword[0] == int(givenPassword)
    
    @staticmethod
    def isEmailExist(email):
        conn, cursor = Dbase.connect()

        sql = 'SELECT COUNT(*) FROM dispatch WHERE email = ?'

        cursor.execute(sql, (email,))
        result = cursor.fetchone()

        Dbase.disconnect(conn, cursor)

        # Return boolean
        return result[0] > 0
        
    @staticmethod
    def getPin(email):
        check = Dbase.isEmailExist(email)
        if check == True:
            conn, cursor = Dbase.connect()
            
            sql = 'SELECT pin FROM Dispatch where email = ?'
            
            cursor.execute(sql, (email, ))
            result = cursor.fetchone()
            
            Dbase.disconnect(conn, cursor)
            
            return result[0]
        else:
            return "error"
                
#Main method to test the functions
if __name__ == "__main__":
    dbObj = Dbase()
    
    #--------whole database control----------#
    # dbObj.deleteDB()
    # dbObj.setUpDB()
    # dbObj.displayDB()
    
    #---------variables----------#
    a = "Mike Ike"
    b = "zak141"
    c = "mohamedkaid014@gmail.com"
    d = 2010
    doc = "Test Card 4"
    newEmail = "mk.mohamedkaid@gmail.com"
    today_date = date.today().strftime("%m-%d-%Y")
    table = "Dispatch"
    
    
    #--------datab base table functionality----------#
    # dbObj.addDispatcher(a,b,c,d)
    # dbObj.deleteDipatchRec('mohamed')
    # Dbase.displayTable(table)
    # dbObj.addDriver("Mike Sam", newEmail)
    # dbObj.addDcoument(doc,today_date,a)
    # dbObj.getDoc(a)
    # dbObj.logIn(c)
    # dbObj.getDrivers(table, "mohamedkaid014@gmail.com")
    # dbObj.changePassword(c,d,e)
    # dbObj.changeEmail(c,newEmail)
    # dbObj.getDispatchId(c)
    print(dbObj.getPin(c))
    # print(dbObj.getAllDocs(c))