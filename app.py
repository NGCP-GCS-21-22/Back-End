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
from tinydb.table import Table
from tinydb.operations import add
import socket
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
MissionDB = TinyDB('./database/mission.json', indent=2)
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
    "missionStages": {
        "MAC": MissionDB.table('MAC'),
        "MEA": MissionDB.table('MEA'),
        "ERU": MissionDB.table('ERU')
    },
    "general": GeneralDB.table('vehicleGeneral'),
    "geofence": GeneralDB.table('geofence'),
    "geofenceSpecial": GeneralDB.table('geofenceSpecial')
}

SPECIAL_GEOFENCE = {'fireLocation', 'searchArea'}

# create an instance of Query class that can help us search the database
query = Query()






# ************************ API ENDPOINTS ************************ #

# Get data from the vehicles
@app.route("/api/vehicleData/<vehicle>", methods=['GET', 'POST'])
def vehicleData(vehicle: str) -> Response:
    # Only use `frontend` or `vehicles` device types for this query string
    db_type = request.args.get('db_type')

    if request.method == 'GET':
        # Retrieve vehicle data from vehicles JSON
        if db_type == 'vehicles':
            vehicle_body = TABLES["vehicles"][vehicle].all()[0]
            return jsonify(vehicle_body)
          
        # Retrieve vehicle data from general JSON
        if db_type == 'general':
            vehicle_general = TABLES["general"].search(query.vehicle == vehicle)[0]
            return jsonify(vehicle_general)

        vehicle_body = TABLES["vehicles"][vehicle].all()[0]
        vehicle_general = TABLES["general"].search(query.vehicle == vehicle)[0]
        
        for key, value in vehicle_general.items():
            vehicle_body[key] = value
        
        # Merge the two together
        return jsonify(vehicle_body)
    
    
    if request.method == 'POST':
        # Retrieve request body
        request_body: dict = request.get_json(force=True)
        response_body = dict()
        # Get db options & error handling
        
        if db_type not in ["general", "vehicles"]:
            return jsonify({"error": "That was not a valid query string. Use either `general` or `vehicles` for query `db_type` only."}), 400
        if len(request_body.keys()) == 0:
            return jsonify({"error": "Please enter a response body for this request"}), 400
        
        # Loop over all given keys in the request body
        for key, value in request_body.items():
            # Update the general JSON if the `db_type` is 'general'
            if db_type == 'frontend':
                TABLES["general"].update({key: value}, query.vehicle == vehicle)
            # Update the respective vehicle JSON if the `db_type` is 'vehicles'
            if db_type == 'vehicles':
                TABLES["vehicles"][vehicle].update({key: value})
            response_body[key] = value
        
        # Return a successful response
        return jsonify({
            "update": "success!",
            "vehicle": vehicle,
            "dataUpdated": response_body
        })


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
        required_fields = {'coordinates','timeCreated','isKeepIn'}
      
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

        # Add data to database
        TABLES['geofence'].insert(geofence)
        
        return jsonify({
            "update": "success!",
            "dataUpdated": geofence
        }), 200


# Get and Post endpoints for Search Area or Fire Location
@app.route('/api/geofenceSpecial/<type>', methods=['GET', 'POST'])
def searchArea(type: str) -> Response:
    if type not in SPECIAL_GEOFENCE:
        return jsonify({'error': f'Given special geofence type must belong in {SPECIAL_GEOFENCE}'}), 400
  
    # Get searchArea
    if request.method == 'GET':
        searchArea_data = TABLES['geofenceSpecial'].search(query.type == type)[0]

        return jsonify(searchArea_data)

    # Post searchArea
    if request.method == 'POST':
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
        TABLES["searchArea"].update({key: request_body[key]}, query.type == type)

    
    # Return a successful response
    return jsonify({
        "update": "success!",
        "dataUpdated": request_body
    })


# Get the predefined mission stages for each vehicle, as well as their associated ID
@app.route('/api/missionStages/<vehicle>', methods=['GET'])
def mission_stages(vehicle: str) -> Response:
    if request.method == 'GET':
        stage_id = request.args.get('id')
        
        if stage_id:
          mission_stage = TABLES['missionStages'][vehicle].search(query.id == int(stage_id))
          return jsonify(mission_stage[0])
        else:
          mission_stage = TABLES['missionStages'][vehicle].all()
          return jsonify(mission_stage)


# Get & update the current stage ID for each vehicle
@app.route('/api/currentStage/<vehicle>', methods=['GET', 'POST'])
def current_stage(vehicle: str) -> Response:
    if request.method == 'GET':
        response_fields = {'vehicle', 'currentStageId'}

        
        vehicle_general = TABLES["general"].search(query.vehicle == vehicle)[0]
        return jsonify({key:vehicle_general[key] for key in response_fields})
    
    
    if request.method == 'POST':
        request_body: dict = request.get_json(force=True)
        
        # Validate whether the indicated mission stage ID actually exists for said vehicle
        try:
            mission_stage = TABLES['missionStages'][vehicle] \
                .search(query.id == request_body["currentStageId"])[0]
        except IndexError:
            return jsonify(
              {"error": f"The requested stage ID does not exists for vehicle `{vehicle}`"}
            ), 400
        
        # Update the stage ID for the indicated vehicle
        TABLES['general'].update(request_body, query.vehicle == vehicle)
        
        # Respond with a success message
        return jsonify({
          "update": "success!",
          "dataUpdated": {
            "vehicle": vehicle,
            "stageId": mission_stage['id'],
            "stageName": mission_stage['name']
          }
        })


# Retrieve & update the mission waypoint for each vehicle
@app.route('/api/missionWaypoint/<vehicle>', methods=['GET', 'POST', 'DELETE'])
def mission_waypoints(vehicle: str) -> Response:
    if request.method == 'GET':
        vehicle_general = TABLES['general'].search(query.vehicle == vehicle)[0]
        
        # Sort the waypoints by time created
        vehicle_waypoint_chronological = sorted(
          vehicle_general["missionWaypoints"],
          key=(lambda waypoint: waypoint['timeCreated'])
        )
        
        return jsonify({
          "vehicle": vehicle_general["vehicle"],
          "missionWaypoints": vehicle_waypoint_chronological
        })
    
    
    if request.method == 'POST':
          request_body: dict = request.get_json(force=True)
        
          # Add new waypoint to the mission waypoints array for the specified vehicle
          TABLES['general'].update(add('missionWaypoints', [request_body]), query.vehicle == vehicle)
        
          return jsonify({
              "update": "success!",
              "dataUpdated": {
                  "vehicle": vehicle,
                  "waypoint": request_body 
              }
          })
        
    
    if request.method == 'DELETE':
        # Delete all waypoints for the specified vehicles
        TABLES["general"].update({'missionWaypoints': []}, query.vehicle == vehicle)
        
        return jsonify({"update": "success!"})




if __name__ == '__main__':

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
    
    external_ip = socket.gethostbyname(socket.gethostname())
    
    print(f"\nExternal IP address: {external_ip}\n")
    app.run(host="0.0.0.0")