
from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS, cross_origin
from updateVehicle import *
from vehicleDatabase import *
from generalStage import *
from datetime import datetime
from mission import *
from urllib import response
from tinydb import TinyDB, Query
import json

# Comment out for testing for frontend 
import sampleGCS

import xbee
import os

app = Flask(__name__)
cors = CORS(app)

# Comment out for testing for frontend 
sampleGCS.getPacket.start_receiving()


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


@app.route("/send", methods = ["POST", "GET"])

def send():
    if (request.method == "POST"):
        requestData = request.get_json()

        # OLD ENDPOINT : postData
        if requestData['id'] == "GET Vehicle Data":
            
            # Initialize the requested vehicle name
            dataInfo = requestData['data']
            vehicleName = dataInfo['vehicle_name']
            # Comment out for testing for frontend 
            ########################################################
            # if send is true
            
            # time.sleep(1)
            ########################################################
            # Query the database for the requested vehicle & save into dictionary
            requestedVehicle = vehicleDatabase.getData(vehicleName)

            # print(requestedVehicle)

            # Send JSON Object back to frontend
            return jsonify(requestedVehicle)
        
        # OLD ENDPOINT: updateGeneralStage
        elif requestData['id'] == "Stage Selection":
            now = datetime.now()
            # Object from frontened
            # requestData = request.get_json()

            #sampleGCS.getPacket.getName(postData.vehicleName)
            #print(now)
            #print(requestData)
            # print(requestData['data'])
            updateStage.updateTime(requestData['data'], now)
            dataInfo = requestData['data']
            sampleGCS.getPacket.getName(dataInfo['vehicle_name'])
            return 'Update Complete'

        # OLD ENDPOINT: getGeneralStage
        elif requestData['id'] == "GET General Stage":
            # opens updateStage.json
            jsonFile = open("updateStage.json")
            dataValue = json.load(jsonFile)

            # Saves the information needed to display general stage
            dataFormat = {
                "id": dataValue['general_stage'],
                "vehicle": dataValue['vehicle'],
                "name": dataValue['stage_name'],
                "estop": dataValue['estop']
            }
            
            return dataFormat

        # OLD ENDPOINT: createNewMission
        elif requestData['id'] == 'Create New Mission':
            # Object from frontend
            requestData = request.get_json()

            # Sends the new mission to be saved
            Mission.createMission(requestData['data'])

            return 'Created New Mission'

        # OLD ENDPOINT: getNewMission
        elif requestData['id'] == 'GET Primary Mission':
            jsonFile = open("newMission.json")
            dataValue = json.load(jsonFile)

            return dataValue
        
        # OLD ENDPOINT: manualOverride
        elif requestData['id'] == 'Manual Control Override':
            requestData = request.get_json()
            dataInfo = requestData['data']
            vehicleName = dataInfo['vehicle_name']
            mode = dataInfo['mode']

            modeFormat = {
                "vehicle_name": vehicleName,
                "mode": mode
            }
            sampleGCS.getPacket.getName(vehicleName)
            # Write the dictionary to the JSON File
            jsonFile = open("manualOverride.json", "w")
            json.dump(modeFormat, jsonFile)
            jsonFile.close()
            
            return modeFormat


# create db.json file for storing geofence data
db = TinyDB('geoDB.json')

# create tables with specific name and initialize them 
MACTable = db.table('MAC')
ERUTable = db.table('ERU')
MEATable = db.table('MEA')
dropCoordinatesTable = db.table('drop_coordinates')
evacuationCoordinatesTable = db.table('evacuation_coordinates')
searchAreaTable = db.table('search_area_coordinates')

# create an instance of Query class that can help us search the database
query = Query()

############## function for debugging purpose ################
# @app.route('/', methods=['GET', 'POST'])
# def debug():
#     # print(db.all())
#     return json.dumps(MACTable.all())
# mea and eru share the same drop location and evacuation zone 

'''
SUBMIT ALL: clear all data and add new submitted data
DELETE ALL: clear all data and leave it be
'''
@app.route('/gcs/geofence/<vehicle_id>', methods=['GET', 'POST'])
def submit_geofence(vehicle_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        geoData = request.get_json(force=True)
        if vehicle_id == 'MAC':
            MACTable.truncate()
            MACTable.insert(geoData)
        elif vehicle_id == 'ERU':
            ERUTable.truncate()
            ERUTable.insert(geoData)
        elif vehicle_id == 'MEA':
            MEATable.truncate()
            MEATable.insert(geoData)
        response_object['message'] = 'data added!'
    else:
        if vehicle_id == 'MAC':
            result = json.dumps(MACTable.all())
        elif vehicle_id == 'ERU':
            result = json.dumps(ERUTable.all())
        elif vehicle_id == 'MEA':
            result = json.dumps(MEATable.all())
        response_object['data'] = result
    return jsonify(response_object)


@app.route('/gcs/geofence/<vehicle_id>', methods=['DELETE'])
def remove_geofence(vehicle_id):
    if(vehicle_id == 'MAC'):
        MACTable.truncate()
    elif(vehicle_id == 'ERU'):
        ERUTable.truncate()
    elif(vehicle_id == 'MEA'):
        MEATable.truncate()
    else: pass
    return "DELETE SUCCESS"

@app.route('/postDropLocation/<vehicle_id>', methods=['POST'])
def post_drop_location(vehicle_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        drop_coordinates = request.get_json(force=True)
        if(vehicle_id == 'MAC'):
            dropCoordinatesTable.upsert(drop_coordinates, query.vehicle=='MAC')
        elif(vehicle_id == 'ERU'):
            dropCoordinatesTable.upsert(drop_coordinates, query.vehicle=='ERU')
        else: pass
        response_object['message'] = 'data added!'
    return jsonify(response_object)

@app.route('/getDropLocation/<vehicle_id>', methods=['GET'])
def get_drop_location(vehicle_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        if(vehicle_id == 'MAC'):
            result=dropCoordinatesTable.search(query.vehicle == 'MAC')
        elif(vehicle_id == 'ERU'):
            result=dropCoordinatesTable.search(query.vehicle == 'ERU')
        else: pass
        response_object['data'] = result
    return jsonify(response_object)

@app.route('/postEvacuationZone/<vehicle_id>', methods=['POST'])
def post_evacuation_zone(vehicle_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        evacuation_coordinates = request.get_json(force=True)
        if(vehicle_id == 'MEA'):
            evacuationCoordinatesTable.upsert(evacuation_coordinates, query.vehicle=='MEA')
        elif(vehicle_id == 'ERU'):
            evacuationCoordinatesTable.upsert(evacuation_coordinates, query.vehicle=='ERU')
        else: pass
        response_object['message'] = 'data added!'
    return jsonify(response_object)

@app.route('/getEvacuationZone/<vehicle_id>', methods=['GET'])
def get_evacuation_zone(vehicle_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        if(vehicle_id == 'MEA'):
            result=evacuationCoordinatesTable.search(query.vehicle == 'MEA')
        elif(vehicle_id == 'ERU'):
            result=evacuationCoordinatesTable.search(query.vehicle == 'ERU')
        else: pass
        response_object['data'] = result
    return jsonify(response_object)

@app.route('/postSearchArea', methods=['POST'])
def post_search_area():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        search_area_coordinates = request.get_json(force=True)
        searchAreaTable.truncate()
        searchAreaTable.insert(search_area_coordinates)
        response_object['message'] = 'data added!'
    return jsonify(response_object)

@app.route('/getSearchArea', methods=['GET'])
def get_search_area():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        result = json.dumps(searchAreaTable.all())
        response_object['data'] = result
    return jsonify(response_object)



####### commands that modify database without requests
# db.drop_table('_default')
# db.drop_table('search_area_coordinates')


# the host value allows traffic from anywhere to run this 
app.run(host = "0.0.0.0")