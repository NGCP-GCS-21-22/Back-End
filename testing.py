import sqlite3
from sqlite3 import Error
#from updateVehicle import *
import pandas as pd 
from datetime import datetime
import json
import re
from xbee import *
from vehicleDatabase import *
# used for testing 

now = datetime.now()
# print(now)

#####################################################################################
oldTime = now.replace(hour=12, minute=0, second=0, microsecond=0).time()
# the latest stage
generalStage = 0
# hour=14, minute=5, second=0, microsecond=0.replace().time()
# New Time
newestPacketTime = now.strftime("%H:%M:%S")

newData = {"vehicle_name": "testing",
            "altitude": 100.0,
            "altitude_color": "Red",
            "battery": 25.0,
            "time": str(newestPacketTime)}

print(newData)

requestedVehicle = vehicleDatabase.getData("MAC")
# x = newData['time']
# jsonTime = datetime.strptime(x, '%H:%M:%S')
# newTime = jsonTime.time()
# newStage = 1

# print("old info")
# print(oldTime)
# print(generalStage)

# # compare the old time/stage with the new time/stage
# if (newTime > oldTime):
#     oldTime = newTime
#     generalStage = newStage

# print("new info")
# print(oldTime)
# print(generalStage)

#####################################################################################

# Values to create connection to SQLite Database
connection = None
dbFile = "database.db"

connection = sqlite3.connect(dbFile, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
vehicleName = "MAC"
#path = "..\databaseCSV\"
# cursor = connection.cursor()
# vehicleTable = """ CREATE TABLE IF NOT EXISTS """ + str(vehicleName) + """(altitude FLOAT, 
#                                                                 altitude_color TEXT, 
#                                                                 battery FLOAT, 
#                                                                 current_stage INTEGER,
#                                                                 geofence_compliant BOOLEAN, 
#                                                                 geofence_compliant_color TEXT, 
#                                                                 latitude FLOAT, 
#                                                                 longitude FLOAT, 
#                                                                 pitch FLOAT, 
#                                                                 pitch_color TEXT, 
#                                                                 propulsion BOOLEAN,
#                                                                 propulsion_color TEXT,
#                                                                 roll FLOAT, 
#                                                                 roll_color TEXT, 
#                                                                 sensors_ok BOOLEAN, 
#                                                                 speed FLOAT, 
#                                                                 stage_completed BOOLEAN, 
#                                                                 status INTEGER, 
#                                                                 yaw FLOAT, 
#                                                                 time_since_last_packet INTEGER, 
#                                                                 last_packet_time INTEGER, 
#                                                                 time STRING,
#                                                                 stage_name STRING,
#                                                                 mode STRING,
#                                                                 hiker_position_lat FLOAT,
#                                                                 hiker_position_lng FLOAT, 
#                                                                 err_msg STRING
#                                                                 )"""

#             # Creates the table
# cursor.execute(vehicleTable)

# vehicleFormat = {
#             'altitude': 0.0,
#             'altitude_color': 'None',
#             'battery': 0.0,
#             'battery_color': 'None',
#             'current_stage': 0,
#             'geofence_compliant': False,
#             'geofence_compliant_color': 'None',
#             'latitude': 0.0,
#             'longitude': 0.0,
#             'mode':'None',
#             'pitch': 0.0,
#             'pitch_color': 'None',
#             'propulsion': False,
#             'propulsion_color': 'None',
#             'roll': 0.0,
#             'roll_color': 'None',
#             'sensors_ok': False,
#             'speed': 0.0,
#             'stage_completed': False,
#             'status': 0,
#             'yaw': 0.0,
#             'time_since_last_packet': 0,
#             'last_packet_time': 0,
#             'time': '2022-01-01 00:00:00',
#             'stage_name': 'None',
#             'mode': 'Manual',
#             'hiker_position_lat': 2,
#             'hiker_position_lng': 7,
#             'err_msg': 'None'
# }

# executionLine = '''INSERT INTO ''' + str(vehicleName) + '''(altitude, altitude_color, battery, current_stage, geofence_compliant,
#                                                geofence_compliant_color, latitude, longitude, pitch, pitch_color, propulsion, 
#                                                propulsion_color, roll, roll_color, sensors_ok, speed, stage_completed, status, yaw,
#                                                time_since_last_packet, last_packet_time, time, stage_name, mode, hiker_position_lat, hiker_position_lng,
#                                                err_msg) VALUES(:altitude, :altitude_color, :battery, 
#                                                :current_stage, :geofence_compliant, :geofence_compliant_color, :latitude, 
#                                                :longitude, :pitch, :pitch_color, :propulsion, :propulsion_color, :roll, :roll_color, :sensors_ok,
#                                                :speed, :stage_completed, :status, :yaw, :time_since_last_packet, :last_packet_time, :time, :stage_name, :mode,
#                                                :hiker_position_lat, :hiker_position_lng, :err_msg)'''
# cursor.execute(executionLine, vehicleFormat)

databaseLine = "SELECT * FROM " + str(vehicleName)
csvTitle = str(vehicleName) + "_database.csv"
db_file = pd.read_sql_query(databaseLine, connection)
db_file.to_csv( 'databaseCSV/' + csvTitle, index = False)

            
# # Enables SQLite commands
# cursor = connection.cursor()

# x = {
#     'altitude': 87.25, 
#     'current_stage': 0,
#     'time': str(now),
#     'stage_name': "Ready to Start"
# }

# # TEST: Tests creating a table
# testingTable = """ CREATE TABLE IF NOT EXISTS testing(altitude FLOAT, current_stage INTEGER, time STRING, stage_name STRING)"""
# cursor.execute(testingTable)

# execution = '''INSERT INTO testing(altitude, current_stage, time, stage_name) VALUES(:altitude, :current_stage, :time, :stage_name)'''
# cursor.execute(execution, x)

#####################################################################################

# used to create data for frontend

# Values to create connection to SQLite Database
# connection = None
# dbFile = "database.db"
# try: 
#     # Establish connection with SQLite database "database.db"
#     connection = sqlite3.connect(dbFile, isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)

#     # Enables SQLite commands
#     cursor = connection.cursor()

#     # TEST: Tests creating a table
#     # testingTable = """ CREATE TABLE IF NOT EXISTS MEA(latitude FLOAT, longitude FLOAT, battery INT, mode STRING, last_packet_time INTEGER, current_stage INTEGER) """
#     # # # Creates the table
#     # cursor.execute(testingTable)



#     databaseLine = "SELECT * FROM ERU"
#     csvTitle = "ERU_database.csv"
#     db_file = pd.read_sql_query(databaseLine, connection)
#     db_file.to_csv(csvTitle, index = False)
    
#     # how to delete tables 
#     # cursor.execute("DROP table MEA")
    
#     connection.close()

# except Error as e: 
#     print(e)

#####################################################################################

# # testingUpdate.py is for testing dictionary updating 

# # Create vehicle dictionary from vehicleDataFormat.py
# vehicleEntry = vehicleDataFormat.dataFormat()

# # New Entry
# newData = {"vehicle_name": "testing",
# "altitude": 100.0,
# "altitude_color": "Red",
# "battery": 25.0,
# "battery_color": "Yellow"}

# # Initialize requested vehicle 
# vehicleName = newData['vehicle_name']

# # Updates dictionary format with new entry
# vehicleEntry.update(newData)
# # vehicle_name is not required
# vehicleEntry.pop('vehicle_name')

# # Save to database
# #vehicleDatabase.saveData(vehicleEntry, vehicleName)

#######################################################

# t = "'altitude':50.0, 'speed':80, 'orientation': 2"
# #print(t)
# dictionary = dict(subString.split(":") for subString in t.split(","))
# #print(dictionary)
# x = "'altitude':50.0, 'speed':80, 'orientation':{Pitch:20*, Roll:120.0*, Yaw:270.0*}"
# x = x.replace("'orientation'", "", -1)
# x = x.replace("{", "", -1)
# x = x.replace("*", "", -1)
# x = x.removesuffix("}")
# # x = x.remove

# subString.split(":") for subString in t.split(","):
# print(x.split(":"))
# x = x.split(":") 

# res = re.split(':|, ', x)

# for i in res: 
#     print(i)

# print(gcsPacket.orientation)