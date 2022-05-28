import sqlite3
from sqlite3 import Error
import pandas as pd 

# vehicleDatabase.py handles storing vehicle data into a database & getting vehicle data

#if __name__ == '__main__':

# Values to create connection to SQLite Database
connection = None
dbFile = "database.db"


vehicleName = "MEA"

    # Method to save new vehicle dictionary entry to SQLite Database        
try: 
    # Establish connection with SQLite database "database.db"
    connection = sqlite3.connect(dbFile, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
    
    # Enables SQLite commands
    cursor = connection.cursor()

    path = "databaseCSV/"
    databaseLine = "SELECT * FROM " + str(vehicleName)
    csvTitle = str(vehicleName) + "_database.csv"
    
    db_file = pd.read_sql_query(databaseLine, connection)
    db_file.to_csv(path + csvTitle, index = False)

    connection.commit()


except Error as e: 
            print(e)