# vehicleDataFormat.py handles the format for vehicle data and creating setter and getter methods

class vehicleDataFormat():
    
    # Used for setter and getter methods
    def __init__(self):
        self.vehicleFormat = {
            'altitude': 0.0,
            'altitude_color': 'None',
            'battery': 0.0,
            #'battery_color': 'None',
            'current_stage': 0,
            'geofence_compliant': False,
            'geofence_compliant_color': 'None',
            'latitude': 0.0,
            'longitude': 0.0,
            'mode':'None',
            'pitch': 0.0,
            'pitch_color': 'None',
            'propulsion': False,
            'propulsion_color': 'None',
            'roll': 0.0,
            'roll_color': 'None',
            'sensors_ok': False,
            'speed': 0.0,
            'stage_completed': False,
            'status': 0,
            'yaw': 0.0,
            'time_since_last_packet': 0,
            'last_packet_time': 0,
            'time': "2022-01-01 00:00:00",
            'stage_name': 'None',
            'hiker_position_lat': 0.0,
            'hiker_position_lng': 0.0,
            'err_msg': 'None'
            # 'hiker_pos':{
            #     'lat': 0.0,
            #     'lng':0.0
            # },
        }

    # battery and connection(time_since_last_packet) already established frontend 
    # The Vehicle Data Format 
    def dataFormat():
        vehicleFormat = {
            'altitude': 0.0,
            'altitude_color': 'None',
            'battery': 0.0,
            #'battery_color': 'None',
            'current_stage': 0,
            'geofence_compliant': False,
            'geofence_compliant_color': 'None',
            'latitude': 0.0,
            'longitude': 0.0,
            'mode':'None',
            'pitch': 0.0,
            'pitch_color': 'None',
            'propulsion': False,
            'propulsion_color': 'None',
            'roll': 0.0,
            'roll_color': 'None',
            'sensors_ok': False,
            'speed': 0.0,
            'stage_completed': False,
            'status': 0,
            'yaw': 0.0,
            'time_since_last_packet': 0,
            'last_packet_time': 0,
            'time': '2022-01-01 00:00:00',
            'stage_name': 'None',
            'hiker_position_lat': 0.0,
            'hiker_position_lng': 0.0,
            'err_msg': 'None'
        }
        return vehicleFormat

# GENERAL GET METHOD
#    def get_value(self, key):
#        return next(item for item in self if item[str(key)] == key)
    
# GENERAL SET METHOD
#    def set_value(self, key, value):
#        next(item for item in self if item[str(key)] == key).update({key: value})

#    def get_jsonFormat(self):
#       return self.jsonFormat

    # Setters and Getters  
    # TODO: Finish setters and getters for color
    
    def setAltitude(self, altitude):
        # if(type(altitude) == decim):           
        self.update({"altitude": altitude})
        if (altitude <= 80):
            self.update({"altitude_color": 'Red'}) 
        elif (altitude > 80 and altitude < 100):
            self.update({"altitude_color": 'Yellow'})
        elif (altitude >= 100):
            self.update({"altitude_color": 'Green'})

    
    def getAltitude(self):
        return self.get("altitude")

    # #Add "Altitude color" (Subject to change)
    # def setAltitudeColor(self, altitudeColor):
    #     if(type(altitudeColor) == str):           
    #         self.update({"altitude_color": altitudeColor})
    
    # def getAltitudeColor(self):
    #     return self.get("altitude_color")
    
    def setBattery(self, battery):
        if(type(battery) == float):           
            self.update({"battery": battery})
    
    def getBattery(self):
        return self.get("battery")

    # #Add "Battery color" (Subject to change)
    # def setBatteryColor(self, batteryColor):
    #     if(type(batteryColor) == str):           
    #         self.update({"battery_color": batteryColor})
    
    # def getBatteryColor(self):
    #     return self.get("battery_color")

    def setCurrentStage(self, stage):
        if(type(stage) == int):           
            self.update({"current_stage": stage})
    
    def getCurrentStage(self):
        return self.get("current_stage")

    def setGeofenceCompliant(self, isCompliant):
        bool(isCompliant)
        if(type(isCompliant) == bool):           
            self.update({"geofence_compliant": isCompliant})
            if(isCompliant is True):
                self.update({'geofence_compliant_color': 'Green'})
            elif(isCompliant is False):
                self.update({'geofence_compliant_color': 'Yellow'})
    
    def getGeofenceCompliant(self):
        return self.get("geofence_compliant")

    #Add GET "Geofence Compliant color"
    
    def setLatitude(self, latitude):
        if(type(latitude) == float):           
            self.update({"latitude": latitude})
    
    def getLatitude(self):
        return self.get("latitude")
    
    def setLongitude(self, longitude):
        if(type(longitude) == float):           
            self.update({"longitude": longitude})
    
    def getLongitude(self):
        return self.get("longitude")

    def setPitch(self, pitch):
        if(type(pitch) == float):           
            self.update({"pitch": pitch})
            if (pitch < -15 or pitch > 15):
                self.update({"pitch_color": "Red"})
            elif ((pitch > -15 and pitch < -10) or (pitch > 10 and pitch < 15)):
                self.update({"pitch_color": "Yellow"})
            elif (pitch >= -10 and pitch <= 10):
                self.update({"pitch_color": "Green"})
    
    def getPitch(self):
        return self.get("pitch")

    #Add GET "Pitch color" 

    def setPropulsion(self, propulsion):
        bool(propulsion)
        if(type(propulsion) == bool):           
            self.update({"propulsion": propulsion})
            if(propulsion == True):
                self.update({'propulsion_color': 'Green'})
            elif(propulsion == False):
                self.update({'propulsion_color': 'Yellow'})
    
    def getPropulsion(self):
        return self.get("propulsion")

    #Add GET "Propulsion color" 

    def setRoll(self, roll):
        if(type(roll) == float):           
            self.update({"roll": roll})
            if (roll < -20 or roll > 20):
                self.update({"roll_color": "Red"})
            elif ((roll > -20 and roll < -15) or (roll > 15 and roll < 20)):
                self.update({"roll_color": "Yellow"})
            elif (roll >= -15 and roll <= 15):
                self.update({"roll_color": "Green"})
    
    def getRoll(self):
        return self.get("roll")

    #Add GET "Roll color" 

    def setSensorsOk(self, sensorOk):
        bool(sensorOk)
        if(type(sensorOk) == bool):           
            self.update({"sensors_ok": sensorOk})
    
    def getSensorsOk(self):
        return self.get("sensors_ok")
    
    def setSpeed(self, speed):
        # if(type(speed) == float):           
        self.update({"speed": speed})
    
    def getSpeed(self):
        return self.get("speed")

    def setStageCompleted(self, stageComplete):
        bool(stageComplete)
        if(type(stageComplete) == bool):           
            self.update({"stage_completed": stageComplete})
    
    def getStageCompleted(self):
        return self.get("stage_completed")

    def setStatus(self, status):
        if(type(status) == int):           
            self.update({"status": status})
    
    def getStatus(self):
        return self.get("status")
        
    def setYaw(self, yaw):
        if(type(yaw) == float):           
            self.update({"yaw": yaw})
    
    def getYaw(self):
        return self.get("yaw")

    def setTimeSinceLastPacket(self, timeSinceLastPacket):
        if(type(timeSinceLastPacket) == int):           
            self.update({"time_since_last_packet": timeSinceLastPacket})
    
    def getTimeSinceLastPacket(self):
        return self.get("time_since_last_packet")
    
    def setLastPacketTime(self, lastPacketTime):
        if(type(lastPacketTime) == int):           
            self.update({"last_packet_time": lastPacketTime})
    
    def getLastPacketTime(self):
        return self.get("last_packet_time")

    def setTime(self, time):
        if(type(time) == str):           
            self.update({"time": time})
    
    def getTime(self):
        return self.get("time")

    def setStageName(self, stageName):
        if(type(stageName) == str):           
            self.update({"stage_name": stageName})
    
    def getStageName(self):
        return self.get("stage_name")

    def setMode(self, mode):
        if(type(mode) == str):           
            self.update({"mode": mode})
    
    def getMode(self):
        return self.get("mode")

    def setHikerPositionLat(self, hikerLat):
        if(type(hikerLat) == float):           
            self.update({"hiker_position_lat": hikerLat})
    
    def getHikerPositionLat(self):
        return self.get("latitude")
    
    def setHikerPositionLng(self, hikerLng):
        if(type(hikerLng) == float):           
            self.update({"hiker_position_lng": hikerLng})
    
    def getHikerPositionLng(self):
        return self.get("hiker_position_lng")

    def setError(self, error):
        if(type(error) == str):           
            self.update({"err_msg": error})
    
    def getError(self):
        return self.get("err_msg")