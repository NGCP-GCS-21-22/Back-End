from http import client
from flask import Flask, Response, g, redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
from updateVehicle import *
from vehicleDatabase import *
from generalStage import *
from datetime import datetime
from mission import *
from urllib import response
from tinydb import TinyDB, Query
import json
import multiprocessing
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double
from utilities import Controller
#from process import Process
import multiprocessing
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double, c_char_p
from utilities import Controller
#from process import Process

# Comment out for testing for frontend
from sampleGCS import Xbee, updateDatabase
import xbee
import os
import time

# Defining the Flask server
app = Flask(__name__)
cors = CORS(app, max_age=600)
app.config['CORS_HEADERS'] = 'Content-Type'



# Extract TinyDB objects from the JSON files
GeneralDB = TinyDB('./database/general.json', indent=2)
MACdb = TinyDB('./database/MAC.json', indent=2)
ERUdb = TinyDB('./database/ERU.json', indent=2)
MEAdb = TinyDB('./database/MEA.json', indent=2)


# Create tables with specific name and initialize them
TABLES = {
    "vehicles": {
      "MAC": MACdb.table('vehicleData'),
      "MEA": MEAdb.table('vehicleData'),
      "ERU": ERUdb.table('vehicleData'),
    },
    "general": GeneralDB.table('vehicleGeneral'),
    "geofence": GeneralDB.table('geofence'),
    "searchArea": GeneralDB.table('searchArea')
}

# create an instance of Query class that can help us search the database
query = Query()


# ************************ API ENDPOINTS ************************ #

# Manual override all vehicles by changing `manualMode` to true
@app.route("/api/manualOverride", methods=['POST'])
def manual_override_all() -> Response:
    # Update the manual control for all vehicle
    TABLES['general'].update({"manualMode": True})
    # Return a success message
    return jsonify({"update": "success!"})


# Manual override specific vehicles by changing `manualMode` to true
@app.route("/api/manualOverride/<vehicle>", methods=['GET', 'POST'])
def manual_override_vehicle(vehicle: str) -> Response:
    if request.method == 'GET':
        # TinyDB search() returns an list, so we have to extract the final dict
        vehicleObject = TABLES["general"].search(query.vehicle == vehicle)[0]
        return jsonify({
            "vehicle": vehicle,
            "manualMode": vehicleObject['manualMode']
        })
  
    if request.method == 'POST':
        TABLES["general"].update({"manualMode": True}, query.vehicle == vehicle)
        return jsonify({"update": "success!"})


# Post data to all vehicles (only general.json)
@app.route("/api/vehicleData", methods=['POST'])
def post_all_vehicle_data():
    # Retrieve request body
    request_body, response_body = request.get_json(force=True), {}
    
    # Basic error handling
    if len(request_body.keys()) == 0:
        return jsonify({"error": "Please enter a response body for this request"}), 400
    
    # Update data for all vehicles (general.json only)
    for key in request_body.keys():
        TABLES["general"].update({key: request_body[key]})
        response_body[key] = request_body[key]
    
    # Return a successful response
    return jsonify({
        "update": "success!",
        "dataUpdated": response_body
    })


# Get data from the vehicles
@app.route("/api/vehicleData/<vehicle>", methods=['GET', 'POST'])
def vehicle_data(vehicle: str) -> Response:
    if request.method == 'GET':
        # Retrieve data from vehicles JSON
        response_body = TABLES["vehicles"][vehicle].all()[0]
        # Retrieve vehicle data from general JSON
        vehicle_general = TABLES["general"].search(query.vehicle == vehicle)[0]
        # Merge the two together
        for key in vehicle_general.keys():
            response_body[key] = vehicle_general[key] 
        return jsonify(response_body)
    
    
    if request.method == 'POST':
        # Retrieve request body
        request_body, response_body = request.get_json(force=True), {}
        
        # Get db options & error handling
        # Only use `general` or `vehicles` for this query string
        db_type = request.args.get('db_type')
        if db_type not in ["general", "vehicles"]:
            return jsonify({"error": "That was not a valid query string. Use either `general` or `vehicles` for query `db_type` only."}), 400
        if len(request_body.keys()) == 0:
            return jsonify({"error": "Please enter a response body for this request"}), 400
        
        # Loop over all given keys in the request body
        for key in request_body.keys():
            # Update the general JSON if the `db_type` is 'general'
            if db_type == 'general':
                TABLES["general"].update({key: request_body[key]}, query.vehicle == vehicle)
            # Update the respective vehicle JSON if the `db_type` is 'vehicles'
            if db_type == 'vehicles':
                TABLES["vehicles"][vehicle]({key: request_body[key]})
            response_body[key] = request_body[key]
        
        # Return a successful response
        return jsonify({
            "update": "success!",
            "vehicle": vehicle,
            "dataUpdated": response_body
        })


# Get and Post GeoFence endpoint
@app.route('/api/geofence', methods=['GET','POST'])
def geofence() -> Response:
    # GET geofence
    if request.method == 'GET':
        # Get all geofence data
        geofence_data = TABLES['geofence'].all()

        # Return geofence data
        return jsonify(geofence_data)
    
    # POST geofence
    if request.method == 'POST':
        required_fields = set(['coordinates','timeCreated','isKeepIn'])
      
        request_body = request.get_json(force=True)
        
        # Validate geofence object
        if not request_body:
            return jsonify({"error": "No data provided"}), 400

        # Get the request body
        geofence = request_body

        # Validate POST request general format
        if not geofence:
            return jsonify({"error": "No geofence data provided"}), 400
        if not isinstance(geofence, dict):
            return jsonify({"error": "Invalid geofence data format"}), 400
        
        # Make sure the request has all required fields  
        if set(geofence.keys()) != required_fields:
            return jsonify({"error": "Invalid geofence data fields. Required fields are {}".format(required_fields)}), 400
        
        for key, value in geofence.items():
            # Validate isKeepIn format
            if key == "isKeepIn":
                if not isinstance(value, bool):
                    return jsonify({"error": "isKeepIn value must be a boolean."}), 400
            
            # Validate timeCreated format
            if key == "timeCreated":
                try:
                    datetime.strptime(value, '%H:%M:%S')
                except ValueError:
                    return jsonify({"error": "Invalid timeCreated format. Must be in HH:MM:SS format"}), 400
            
            # Validate coordinates format
            if key == "coordinates":
                coords = value 
                # Check for minimum number of coordinates and list format
                if not isinstance(coords, list) or len(coords) < 3:
                    return jsonify({"error": "Geofence data coordinates must be a list of at least 3 coordinates"}), 400
                
                for coord in coords:
                    # Check format of each coordinate sets
                    if not isinstance(coord, dict) or 'lat' not in coord or 'lng' not in coord:
                        return jsonify({"error": "Invalid geofence coordinates format"}), 400
                    # Validate latitude and longitude
                    if not (-90 <= coord['lat'] <= 90 and -180 <= coord['lng'] <= 180):
                        return jsonify({"error": "Invalid geofence coordinates range latitude:[-90,90] and longitude:[-180,180]"}), 400

        #Add data to database
        TABLES['geofence'].insert(geofence)
        
        return jsonify({
            "update": "success!",
            "dataUpdated": geofence
        }), 200

# Get and Post Search Area
@app.route('/api/searchArea', methods = ['GET', 'POST'])
def searchArea():
    # Get searchArea
    if request.method == 'GET':
        searchArea_data = TABLES['searchArea'].all()[0]

        return jsonify(searchArea_data)

    # Post searchArea
    if request.method == 'POST':
        required_fields = 'coordinates'
        request_body = request.get_json(force=True)

        # Verify only one response body is passed in
        if len(request_body.keys()) != 1:
            return jsonify({"error": "Please enter a valid response body for this request"}), 400

        # Validate coordinates format
        key = next(iter(request_body.keys()))
        if key == "coordinates":
            coords = request_body[key] 
            # Check for minimum number of coordinates and list format
            if not isinstance(coords, list) or len(coords) < 3:
                return jsonify({"error": "Search Area data coordinates must be a list of at least 3 coordinates"}), 400
            
            for coord in coords:
                # Check format of each coordinate sets
                if not isinstance(coord, dict) or 'lat' not in coord or 'lng' not in coord:
                    return jsonify({"error": "Invalid search area coordinates format"}), 400
                # Validate latitude and longitude
                if not (-90 <= coord['lat'] <= 90 and -180 <= coord['lng'] <= 180):
                    return jsonify({"error": "Invalid search area coordinates range latitude:[-90,90] and longitude:[-180,180]"}), 400
                
        #Update searchArea in database
        TABLES["searchArea"].update({key: request_body[key]})

    
    # Return a successful response
    return jsonify({
        "update": "success!",
        "dataUpdated": request_body
    })

if __name__ == '__main__':
    #============= Shared Memory ===============#

    controller_data = Array('i', [0] * 8)
    controller_process = multiprocessing.Process(
      target=Controller.run_controller,
      args = (False, controller_data)
    )
    controller_process.start()
    
    #============== App =======================#

    # Comment out for testing for frontend
    manager = multiprocessing.Manager()
    # xbee_data = manager.list([0]*17)
    # xbee_send_data = manager.list([0]*10)
    send_flag = Value('B', 0)
    receive_flag = Value('B', 0)
    vehicleName = manager.Value(c_char_p, "ERU")

    # xbee_process = multiprocessing.Process(target=Xbee.xbee_run, 
    #                                        args = (xbee_data, send_flag, receive_flag, vehicleName, 
    #                                                xbee_send_data, controller_data))
    # xbee_process.start()
    #print(xbee_data[:])
    
    # vehicleName.value = "ERU"
    # while True:
    #     print(controller_data[:])
    #     print(xbee_data[:])
    #     time.sleep(2)
    #     send_flag.value = 1
    #     print(send_flag.value)
# Comment out for testing for frontend



    #============== App =======================#



    # Comment out for testing for frontend
    # sampleGCS = getPacket()
    # sampleGCS.initialize_comms()
    # sampleGCS.start_receiving()
    #sampleGCS.getPacket.start_receiving()

        #print("Axis: " + str(controller_data[0]))
        #print()


# # Update the database with new entries
# @app.route("/sendData", methods = ["POST"])
# def sendData():
#     if(request.method == "POST"):
#         # Object from comm
#         requestData = request.get_json()

#         # Initialize the requested vehicle name
#         vehicleName = requestData['vehicle_name']
#         #newTime = requestData['time']

#         # Initialize the vehicle datapoints
#         altitude = requestData['altitude']
#         #altitudeColor = requestData ['altitude_color']
#         battery = requestData['battery']
#         #batteryColor = requestData['battery_color']
#         currentStage = requestData['current_stage']
#         geofenceCompilant = requestData['geofence_compliant']
#         bool(geofenceCompilant)
#         #geofenceCompilantColor = requestData['geofence_compliant_color']
#         latitude = requestData['latitude']
#         longitude = requestData['longitude']
#         pitch = requestData['pitch']
#         #pitchColor = requestData['pitch_color']
#         propulsion = requestData['propulsion']
#         roll = requestData['roll']
#         #rollColor = requestData['roll_color']
#         sensorsOk = requestData['sensors_ok']
#         speed = requestData['speed']
#         stageComplete = requestData['stage_completed']
#         status = requestData['status']
#         yaw = requestData['yaw']
#         timeSinceLastPacket = requestData['time_since_last_packet']
#         lastPacketTime = requestData['last_packet_time']
#         time = requestData['time']

#         # Gets the stage name of the sent stage id
#         stageName = updateStage.updateStageName(currentStage)

#         # Update the vehicle dictionary with given values
#         requestedVehicle = updateVehicle.newAltitude(altitude)
#         #requestedVehicle = updateVehicle.newAltitudeColor(altitudeColor)
#         requestedVehicle = updateVehicle.newBattery(battery)
#         #requestedVehicle = updateVehicle.newBatteryColor(batteryColor)
#         requestedVehicle = updateVehicle.newCurrentStage(currentStage)
#         requestedVehicle = updateVehicle.newGeofenceCompilant(geofenceCompilant)
#         #requestedVehicle = updateVehicle.newGeofenceCompilantColor(geofenceCompilantColor)
#         requestedVehicle = updateVehicle.newLatitude(latitude)
#         requestedVehicle = updateVehicle.newLongitude(longitude)
#         requestedVehicle = updateVehicle.newPitch(pitch)
#         #requestedVehicle = updateVehicle.newPitchColor(pitchColor)
#         requestedVehicle = updateVehicle.newPropulsion(propulsion)
#         requestedVehicle = updateVehicle.newRoll(roll)
#         #requestedVehicle = updateVehicle.newRollColor(rollColor)
#         requestedVehicle = updateVehicle.newSensorsOk(sensorsOk)
#         requestedVehicle = updateVehicle.newSpeed(speed)
#         requestedVehicle = updateVehicle.newStageCompleted(stageComplete)
#         requestedVehicle = updateVehicle.newStatus(status)
#         requestedVehicle = updateVehicle.newYaw(yaw)
#         requestedVehicle = updateVehicle.newTimeSinceLastPacket(timeSinceLastPacket)
#         requestedVehicle = updateVehicle.newLastPacketTime(lastPacketTime)
#         requestedVehicle = updateVehicle.newTime(time)
#         requestedVehicle = updateVehicle.newStageName(stageName)

#         # Save the vehicle dictionary into SQLite Database
#         vehicleDatabase.saveData(requestedVehicle, vehicleName)


#         # TEST: show that the vehicle dictionary has been saved correctly
#         return geofenceCompilant
#         #return '''The value is: {}'''.format(requestedVehicle)

# Sends back the latest entry from requested vehicle
# @app.route("/postData", methods = ["POST"])
# def postData():

#     if(request.method == "POST"):
#         # JSON Format from frontend
#         requestData = request.get_json()

#         # Initialize the requested vehicle name
#         vehicleName = requestData['vehicle_name']

#         # Comment out for testing for frontend
#         ########################################################
#         # if send is true
#         # sampleGCS.getPacket.getName(vehicleName)
#         # time.sleep(1)
#         ########################################################
#         # Query the database for the requested vehicle & save into dictionary
#         requestedVehicle = vehicleDatabase.getData(vehicleName)

#         # print(requestedVehicle)

#         # Send JSON Object back to frontend
#         return jsonify(requestedVehicle)

# Compares new request's stage/time to updateStage.json
# @app.route("/updateGeneralStage", methods = ['POST'])
# def updateGeneralStage():
#     if(request.method == "POST"):


#         now = datetime.now()
#         # Object from frontened
#         requestData = request.get_json()

#         #sampleGCS.getPacket.getName(postData.vehicleName)
#         #print(now)
#         #print(requestData)
#         updateStage.updateTime(requestData, now)

#     return 'Update Complete'

# Sends information from updateStage.json
# @app.route("/getGeneralStage", methods = ['GET'])
# def getGeneralStage():

#     # opens updateStage.json
#     jsonFile = open("updateStage.json")
#     dataValue = json.load(jsonFile)

#     # Saves the information needed to display general stage
#     dataFormat = {
#         "id": dataValue['general_stage'],
#         "vehicle": dataValue['vehicle'],
#         "name": dataValue['stage_name'],
#         "estop": dataValue['estop']
#     }

#     return dataFormat

# Saves the new mission entry into newMission.json
# @app.route("/createNewMission", methods = ['POST'])
# def createNewMission():
#     if(request.method == "POST"):

#         # Object from frontend
#         requestData = request.get_json()

#         # Sends the new mission to be saved
#         Mission.createMission(requestData)

#     return 'Created New Mission'

# Sends back the saved mission from newMission.json
# @app.route("/getNewMission", methods = ['GET'])
# def getnewMission():
#     if(request.method == "GET"):
#         # Opens the saved mission entry from the JSON File and saves it into a variable


#         jsonFile = open("newMission.json")
#         dataValue = json.load(jsonFile)

#     return dataValue

# @app.route("/manualOverride", methods = ['POST'])
# def manualOverride():
#     if(request.method == "POST"):

#         requestData = request.get_json()
#         vehicleName = requestData['vehicle_name']
#         mode = requestData['mode']

#         modeFormat = {
#             "vehicle_name": vehicleName,
#             "mode": mode
#         }

#         # Write the dictionary to the JSON File
#         jsonFile = open("manualOverride.json", "w")
#         json.dump(modeFormat, jsonFile)
#         jsonFile.close()
#     return modeFormat


    # @app.route("/send", methods = ["POST", "GET"])
    # def send():
    #     now = datetime.now()
    #     if (request.method == "POST"):
    #         requestData = request.get_json()

    #         # OLD ENDPOINT : postData
    #         if requestData['id'] == "GET Vehicle Data":

    #             # Initialize the requested vehicle name
    #             dataInfo = requestData['data']
    #             vehicleName.value = dataInfo['vehicle_name']
    #             # Comment out for testing for frontend
    #             ########################################################
    #             # if send is true
    #             # sampleGCS.getName(vehicleName, controller_data[0], controller_data[1], controller_data[2], 
    #             #                                 controller_data[3], controller_data[4], controller_data[5], 
    #             #                                 bool(controller_data[6]), bool(controller_data[7]))

    #             send_flag.value = 1
    #             if receive_flag.value == 1:
    #                 dataInfo = requestData['data']
    #                 vehicleName.value = dataInfo['vehicle_name']
    #                 receive_flag.value = 0
    #             # time.sleep(1)
    #             ########################################################
    #             # Query the database for the requested vehicle & save into dictionary
    #             requestedVehicle = vehicleDatabase.getData(vehicleName.value)

    #             # print(requestedVehicle)

    #             # Send JSON Object back to frontend
    #             return jsonify(requestedVehicle)

    #         # OLD ENDPOINT: updateGeneralStage
    #         elif requestData['id'] == "Stage Selection":
    #             now = datetime.now()
    #             # Object from frontened
    #             # requestData = request.get_json()

    #             # ============ Send manual control data =============#
    #             # sampleGCS.getName(postData.vehicleName, controller_data[0], controller_data[1], controller_data[2], 
    #             #                                         controller_data[3], controller_data[4], controller_data[5], 
    #             #                                         bool(controller_data[6]), bool(controller_data[7]))
    #             #print(now)
    #             #print(requestData)
    #             # print(requestData['data'])


    #             updateStage.updateTime(requestData['data'], now)
    #             if receive_flag.value == 1:
    #                 dataInfo = requestData['data']
    #                 vehicleName.value = dataInfo['vehicle_name']
    #                 receive_flag.value = 0

    #             send_flag.value = 1
    #             newestPacketTime = now.strftime("%H:%M:%S")
    #             updateDatabase.newEntries(xbee_data, newestPacketTime, vehicleName.value)
                
    #             return 'Update Complete'

    #         # OLD ENDPOINT: getGeneralStage
    #         elif requestData['id'] == "GET General Stage":
    #             # opens updateStage.json
    #             jsonFile = open("updateStage.json")
    #             dataValue = json.load(jsonFile)

    #             # Saves the information needed to display general stage
    #             dataFormat = {
    #                 "id": dataValue['general_stage'],
    #                 "vehicle": dataValue['vehicle'],
    #                 "name": dataValue['stage_name'],
    #                 "estop": dataValue['estop']
    #             }

    #             return dataFormat

    #         # OLD ENDPOINT: createNewMission
    #         elif requestData['id'] == 'Create New Mission':
    #             # Object from frontend
    #             requestData = request.get_json()

    #             # Sends the new mission to be saved
    #             Mission.createMission(requestData['data'])

    #             return 'Created New Mission'

    #         # OLD ENDPOINT: getNewMission
    #         elif requestData['id'] == 'GET Primary Mission':
    #             jsonFile = open("newMission.json")
    #             dataValue = json.load(jsonFile)

    #             return dataValue

    #         # OLD ENDPOINT: manualOverride
    #         elif requestData['id'] == 'Manual Control Override':
    #             requestData = request.get_json()
    #             dataInfo = requestData['data']
    #             vehicleName.value = dataInfo['vehicle_name']
    #             mode = dataInfo['mode']

    #             modeFormat = {
    #                 "vehicle_name": vehicleName.value,
    #                 "mode": mode
    #             }
                
    #             send_flag.value = 1
    #             if receive_flag.value == 1:
    #                 dataInfo = requestData['data']
    #                 vehicleName.value = dataInfo['vehicle_name']
    #                 receive_flag.value = 0

    #             # sampleGCS.getName(vehicleName, controller_data[0], controller_data[1], controller_data[2], 
    #             #                                 controller_data[3], controller_data[4], controller_data[5], 
    #             #                                 bool(controller_data[6]), bool(controller_data[7]))
    #             # Write the dictionary to the JSON File
    #             jsonFile = open("manualOverride.json", "w")
    #             json.dump(modeFormat, jsonFile)
    #             jsonFile.close()

    #             return modeFormat


    

    def is_empty(result):
        return True if len(result)==0 else False
    def is_correct_coordinates_format(obj):
        if not is_empty(obj):
            # lat = -90 to 90
            # lng = -180 to 180
            if (isinstance(obj["lat"], float)) or (isinstance(obj["lat"], int)):
                if not (-90 <= obj["lat"] <= 90):
                    raise Exception("ERROR: Latitude not valid")
            else:
                raise Exception("ERROR: Latitude not a float")

            if isinstance(obj["lng"], float) or isinstance(obj["lng"], int):
                if not (-180 <= obj["lng"] <= 180):
                    raise Exception("ERROR: Longitude not valid")
            else:
                raise Exception("ERROR: Longitude not a float")
            return True
        return False
    '''
    SUBMIT ALL: clear all data and add new submitted data
    DELETE ALL: clear all data and leave it be
    '''
    # @app.route('/postGeofence/<vehicle_name>', methods=['POST'])
    # def submit_geofence(vehicle_name):
    #     response_object = {'status': 'success'}
    #     if request.method == 'POST':
    #         geoData = request.get_json(force=True)
    #         if vehicle_name == 'MAC':
    #             MACTable.truncate()
    #             MACTable.insert(geoData)
    #         elif vehicle_name == 'ERU':
    #             ERUTable.truncate()
    #             ERUTable.insert(geoData)
    #         elif vehicle_name == 'MEA':
    #             MEATable.truncate()
    #             MEATable.insert(geoData)
    #         response_object['message'] = 'data added!'
    #     return jsonify(response_object)

    # @app.route('/getGeofence/<vehicle_name>', methods=['GET'])
    # def get_geofence(vehicle_name):
    #     result={}
    #     if vehicle_name == 'MAC':
    #         result = MACTable.all()
    #     elif vehicle_name == 'ERU':
    #         result = ERUTable.all()
    #     elif vehicle_name == 'MEA':
    #         result = MEATable.all()
    #     return jsonify(result[0]['geofence']) if not is_empty(result) else jsonify([])

    # @app.route('/gcs/geofence/<vehicle_id>', methods=['DELETE'])
    # def remove_geofence(vehicle_id):
    #     if(vehicle_id == 'MAC'):
    #         MACTable.truncate()
    #     elif(vehicle_id == 'ERU'):
    #         ERUTable.truncate()
    #     elif(vehicle_id == 'MEA'):
    #         MEATable.truncate()
    #     else: pass
    #     return "DELETE SUCCESS"

    # @app.route('/postERUDropLocation', methods=['POST'])
    # def post_drop_location():
    #     response_object = {'status': 'success'}
    #     drop_coordinates = request.get_json(force=True)
    #     if is_correct_coordinates_format(drop_coordinates):
    #         dropCoordinatesTable.truncate()
    #         dropCoordinatesTable.insert(drop_coordinates)
    #         response_object['message'] = 'data added!'
    #     return jsonify(response_object)

    # @app.route('/postEvacuationZone', methods=['POST'])
    # def post_evacuation_zone():
    #     response_object = {'status': 'success'}
    #     evac_coordinates = request.get_json(force=True)
    #     if is_correct_coordinates_format(evac_coordinates):
    #         evacuationCoordinatesTable.truncate()
    #         evacuationCoordinatesTable.insert(evac_coordinates)
    #         response_object['message'] = 'data added!'
    #     return jsonify(response_object)

    # # return drop location for MAC and evacuation zone for MEA and ERU
    # @app.route('/getMissionWaypoint/<vehicle_name>', methods=['GET'])
    # def get_mission_waypoint(vehicle_name):
    #     result={}
    #     if request.method == 'GET':
    #         if(vehicle_name == 'MAC'):
    #             result = dropCoordinatesTable.all()
    #         elif(vehicle_name == 'MEA' or vehicle_name == 'ERU'):
    #             result = evacuationCoordinatesTable.all()
    #         else: pass
    #     return jsonify(result[0]) if not is_empty(result) else jsonify({})

    # each vechicle has its own home location
    # @app.route('/postHomeCoordinates/<vehicle_name>', methods=['POST'])
    # def post_home_location(vehicle_name):
    #     response_object = {'status': 'success'}
    #     home_coordinates = request.get_json(force=True)
    #     if is_correct_coordinates_format(home_coordinates):
    #         if(vehicle_name == 'MAC'):
    #             homeLocationTable.upsert(home_coordinates, query.vehicle=='MAC')
    #         elif(vehicle_name == 'ERU'):
    #             homeLocationTable.upsert(home_coordinates, query.vehicle=='ERU')
    #         elif(vehicle_name == 'MEA'):
    #             homeLocationTable.upsert(home_coordinates, query.vehicle=='MEA')
    #         else: pass
    #         response_object['message'] = 'data added!'
    #     return jsonify(response_object)

    # # each vehicle has its own home location
    # @app.route('/getHomeCoordinates/<vehicle_name>', methods=['GET'])
    # def get_home_location(vehicle_name):
    #     result={}
    #     if request.method == 'GET':
    #         if(vehicle_name == 'MAC'):
    #             result=homeLocationTable.search(query.vehicle == 'MAC')
    #         elif(vehicle_name == 'ERU'):
    #             result=homeLocationTable.search(query.vehicle == 'ERU')
    #         elif(vehicle_name == 'MEA'):
    #             result=homeLocationTable.search(query.vehicle == 'MEA')
    #         else: pass
    #     return jsonify(result[0]) if not is_empty(result) else jsonify({})

    # @app.route('/postSearchArea', methods=['POST'])
    # def post_search_area():
    #     response_object = {'status': 'success'}
    #     if request.method == 'POST':
    #         search_area_coordinates = request.get_json(force=True)
    #         searchAreaTable.truncate()
    #         searchAreaTable.insert(search_area_coordinates)
    #         response_object['message'] = 'data added!'
    #     return jsonify(response_object)

    # @app.route('/getSearchArea', methods=['GET'])
    # def get_search_area():
    #     result={}
    #     if request.method == 'GET':
    #         result = searchAreaTable.all()
    #     return jsonify(result[0]["search_area"]) if not is_empty(result) else jsonify([])


    # the host value allows traffic from anywhere to run this
    app.run(host="0.0.0.0")