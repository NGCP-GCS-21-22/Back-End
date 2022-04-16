import sqlite3
from sqlite3 import Error
import pandas as pd 

# vehicleDatabase.py handles storing vehicle data into a database & getting vehicle data

#if __name__ == '__main__':

# Values to create connection to SQLite Database
connection = None
dbFile = "database.db"


class vehicleDatabase():

    # Method to save new vehicle dictionary entry to SQLite Database
    def saveData(requestedVehicle, vehicleName):        
        try: 
            # Establish connection with SQLite database "database.db"
            connection = sqlite3.connect(dbFile, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
            
            # Enables SQLite commands
            cursor = connection.cursor()

            # TEST: Tests creating a table
            testingTable = """ CREATE TABLE IF NOT EXISTS """ + str(vehicleName) + """(altitude FLOAT, current_stage INTEGER, time STRING, stage_name STRING)"""
            

            # Create an empty table with the vehicle data. 
            # Parameters follow the format (varName, TYPE). 
            vehicleTable = """ CREATE TABLE IF NOT EXISTS """ + str(vehicleName) + """(altitude FLOAT, 
                                                                altitude_color TEXT, 
                                                                battery FLOAT, 
                                                                current_stage INTEGER,
                                                                geofence_compliant BOOLEAN, 
                                                                geofence_compliant_color TEXT, 
                                                                latitude FLOAT, 
                                                                longitude FLOAT, 
                                                                pitch FLOAT, 
                                                                pitch_color TEXT, 
                                                                propulsion BOOLEAN,
                                                                propulsion_color TEXT,
                                                                roll FLOAT, 
                                                                roll_color TEXT, 
                                                                sensors_ok BOOLEAN, 
                                                                speed FLOAT, 
                                                                stage_completed BOOLEAN, 
                                                                status INTEGER, 
                                                                yaw FLOAT, 
                                                                time_since_last_packet INTEGER, 
                                                                last_packet_time INTEGER, 
                                                                time STRING,
                                                                stage_name STRING,
                                                                mode STRING,
                                                                hiker_position_lat FLOAT,
                                                                hiker_position_lng FLOAT, 
                                                                err_msg STRING
                                                                )"""

            # Creates the table
            cursor.execute(vehicleTable)

            # Enters the values into the requested vehicle database
            # executionLine = 'INSERT INTO ' + str(vehicleName) + '(altitude, current_stage, time, stage_name) VALUES(:altitude, :current_stage, :time, :stage_name)'
            # cursor.execute(executionLine, requestedVehicle)

            executionLine = '''INSERT INTO ''' + str(vehicleName) + '''(altitude, altitude_color, battery, current_stage, geofence_compliant,
                                               geofence_compliant_color, latitude, longitude, pitch, pitch_color, propulsion, 
                                               propulsion_color, roll, roll_color, sensors_ok, speed, stage_completed, status, yaw,
                                               time_since_last_packet, last_packet_time, time, stage_name, mode, hiker_position_lat, hiker_position_lng,
                                               err_msg) VALUES(:altitude, :altitude_color, :battery, 
                                               :current_stage, :geofence_compliant, :geofence_compliant_color, :latitude, 
                                               :longitude, :pitch, :pitch_color, :propulsion, :propulsion_color, :roll, :roll_color, :sensors_ok,
                                               :speed, :stage_completed, :status, :yaw, :time_since_last_packet, :last_packet_time, :time, :stage_name, :mode,
                                               :hiker_position_lat, :hiker_position_lng, :err_msg)'''
            cursor.execute(executionLine, requestedVehicle)

            # TEST: Accepting packets under certain conditions
            #if (json1['altitude'] == 1.0):
            #    cursor.execute('INSERT INTO testing(altitude, altitude_color, battery, battery_color) VALUES(:altitude, :altitude_color, :battery, :battery_color)', json1)
            
            # Export the database onto an CSV file

            path = "databaseCSV/"
            databaseLine = "SELECT * FROM " + str(vehicleName)
            csvTitle = str(vehicleName) + "_database.csv"
            
            db_file = pd.read_sql_query(databaseLine, connection)
            db_file.to_csv(path + csvTitle, index = False)

            connection.commit()
            #connection.close()

        except Error as e: 
            print(e)

    def getData(vehicleName):
        # https://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python
        
        try:
            # Establish connection with SQLite database "database.db"
            connection = sqlite3.connect(dbFile, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES) 

            # Enables SQLite commands
            cursor = connection.cursor()

            # Select from the requested vehicle database and get the last entry
            execution_line = "SELECT * FROM " + str(vehicleName) + " ORDER BY rowid DESC LIMIT 1"
            cursor.execute(execution_line)

            # Create a list[dictionary] for the last entry
            lastEntry = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]

            # Extract dictionary from list 
            for entry in lastEntry:
                if entry['longitude'] != None:
                    finalizedEntry = entry
                    break
                else:
                    finalizedEntry = None

            connection.close()

            return finalizedEntry

            #one = False
            #return (lastEntry[0] if lastEntry else None) if one else lastEntry
        except Error as e:
            print(e)

# Used for testing
#x = "testing"
#vehicleDatabase.getData(x)





