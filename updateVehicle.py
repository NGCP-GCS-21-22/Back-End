import json
from vehicleDataFormat import *
from datetime import datetime
from vehicleDatabase import *
from generalStage import *
from xbee import *
# from sampleGCS import *

# updateVehicle.py handles saving new mission entry datapoints to the data format

# Create vehicle dictionary from vehicleDataFormat.py
vehicleEntry = vehicleDataFormat.dataFormat()

class updateVehicle():

    # TODO: add the methods for all datapoints
    
    # Methods to save the new datapoints into the vehicle dictionary
    def newAltitude(altitude):
        vehicleDataFormat.setAltitude(vehicleEntry, altitude)
        return vehicleEntry 

    # Altitude color
    def newAltitudeColor(altitudeColor):
        vehicleDataFormat.setAltitudeColor(vehicleEntry, altitudeColor)
        return vehicleEntry 

    def newBattery(battery):
        vehicleDataFormat.setBattery(vehicleEntry, battery)
        return vehicleEntry
        
    # Battery color 
    # def newBatteryColor(batteryColor):
    #     vehicleDataFormat.setBatteryColor(vehicleEntry, batteryColor)
    #     return vehicleEntry

    def newCurrentStage(stage):
        vehicleDataFormat.setCurrentStage(vehicleEntry, stage)
        return vehicleEntry 

    def newGeofenceCompilant(isCompilant):
        vehicleDataFormat.setGeofenceCompliant(vehicleEntry, isCompilant)
        return vehicleEntry 

    # Geofence Color

    def newLatitude(latitude):
        vehicleDataFormat.setLatitude(vehicleEntry, latitude)
        return vehicleEntry 

    def newLongitude(longitude):
        vehicleDataFormat.setLongitude(vehicleEntry, longitude)
        return vehicleEntry 

    def newPitch(pitch):
        vehicleDataFormat.setPitch(vehicleEntry, pitch)
        return vehicleEntry 

    # Pitch color

    def newPropulsion(propulsion):
        vehicleDataFormat.setPropulsion(vehicleEntry, propulsion)
        return vehicleEntry 
    
    # Propulsion Color

    def newRoll(roll):
        vehicleDataFormat.setRoll(vehicleEntry, roll)
        return vehicleEntry 
    
    # Roll Color

    def newSensorsOk(sensorOk):
        vehicleDataFormat.setSensorsOk(vehicleEntry, sensorOk)
        return vehicleEntry 

    def newSpeed(speed):
        vehicleDataFormat.setSpeed(vehicleEntry, speed)
        return vehicleEntry

    def newStageCompleted(stageComplete):
        vehicleDataFormat.setStageCompleted(vehicleEntry, stageComplete)
        return vehicleEntry

    def newStatus(status):
        vehicleDataFormat.setStatus(vehicleEntry, status)
        return vehicleEntry
    
    def newYaw(yaw):
        vehicleDataFormat.setYaw(vehicleEntry, yaw)
        return vehicleEntry

    def newTimeSinceLastPacket(timeSinceLastPacket):
        vehicleDataFormat.setTimeSinceLastPacket(vehicleEntry, timeSinceLastPacket)
        return vehicleEntry

    def newLastPacketTime(lastPacketTime):
        vehicleDataFormat.setLastPacketTime(vehicleEntry, lastPacketTime)
        return vehicleEntry

    def newTime(time):
        vehicleDataFormat.setTime(vehicleEntry, time)
        return vehicleEntry

    def newStageName(stageName):
        vehicleDataFormat.setStageName(vehicleEntry, stageName)
        return vehicleEntry

    def newMode(mode):
        vehicleDataFormat.setMode(vehicleEntry, mode)
        return vehicleEntry
    
    def newHikerPositionLat(hikerLat):
        vehicleDataFormat.setHikerPositionLat(vehicleEntry, hikerLat)
        return vehicleEntry
    
    def newHikerPositionLng(hikerLng):
        vehicleDataFormat.setHikerPositionLng(vehicleEntry, hikerLng)
        return vehicleEntry

    def newErrMsg(error):
        vehicleDataFormat.setHikerPositionLng(vehicleEntry, error)
        return vehicleEntry

# ask matthew about this 
# Autonomous
# Manual
