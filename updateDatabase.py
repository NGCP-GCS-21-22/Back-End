import json
from vehicleDataFormat import *
from datetime import datetime
from vehicleDatabase import *
from generalStage import *
#from xbee import *
#import sampleGCS
import updateVehicle

from queue import Empty
import time
from digi.xbee.devices import DigiMeshDevice
import xbee
from xbee import TransmitThread, read_lock, ToERU, ToMAC, ToGCS, Orientation, LatLng, ManualControl, Geofence, SearchArea
import threading
import struct

class updateDatabase():
    #vehicleDatabase()
    def newEntries(cls):
        # call updateVehicle class 
        #updateVehicle()

        print(gcsPacket + "hi")
        vehicleFormat = {
            'vehicle_name': 'MAC',
            'altitude': gcsPacket.altitude,
            'altitude_color': 'None',
            'battery': gcsPacket.battery,
            #'battery_color': 'None',
            'current_stage': gcsPacket.current_state,
            'geofence_compliant': gcsPacket.geofence_compliant,
            'geofence_compliant_color': 'None',
            'latitude': gcsPacket.gps.lat,
            'longitude': gcsPacket.gps.lng,
            'mode':'Manual',
            'pitch': gcsPacket.orientation.pitch,
            'pitch_color': 'None',
            'propulsion': gcsPacket.propulsion,
            'propulsion_color': 'None',
            'roll': gcsPacket.orientation.roll,
            'roll_color': 'None',
            'sensors_ok': gcsPacket.sensors_ok,
            'speed': gcsPacket.speed,
            'stage_completed': gcsPacket.state_complete,
            'status': gcsPacket.status,
            'yaw': gcsPacket.orientation.yaw,
            'time_since_last_packet': 78,
            'last_packet_time': 100,
            # need to add this to comms 
            'time': '2022-01-01 00:00:00',
            'stage_name': 'None'
        }

        # Initialize the requested vehicle name
        vehicleName = vehicleFormat['vehicle_name']

        # Initialize the vehicle datapoints  
        altitude = vehicleFormat['altitude']
        battery = vehicleFormat['battery']
        currentStage = vehicleFormat['current_stage']
        geofenceCompilant = vehicleFormat['geofence_compliant']
        latitude = vehicleFormat['latitude']
        longitude = vehicleFormat['longitude']
        pitch = vehicleFormat['pitch']
        propulsion = vehicleFormat['propulsion']
        roll = vehicleFormat['roll']
        sensorsOk = vehicleFormat['sensors_ok']
        speed = vehicleFormat['speed']
        stageComplete = vehicleFormat['stage_completed']
        status = vehicleFormat['status']
        yaw = vehicleFormat['yaw']
        timeSinceLastPacket = vehicleFormat['time_since_last_packet']
        lastPacketTime = vehicleFormat['last_packet_time']
        time = vehicleFormat['time']
        mode = vehicleFormat['mode']

        # Gets the stage name of the sent stage id 
        stageName = updateStage.updateStageName(currentStage)
        
        # Update the vehicle dictionary with given values 
        requestedVehicle = updateVehicle.newAltitude(altitude)
        requestedVehicle = updateVehicle.newBattery(battery)
        requestedVehicle = updateVehicle.newCurrentStage(currentStage)
        requestedVehicle = updateVehicle.newGeofenceCompilant(geofenceCompilant)
        requestedVehicle = updateVehicle.newLatitude(latitude)
        requestedVehicle = updateVehicle.newLongitude(longitude)
        requestedVehicle = updateVehicle.newPitch(pitch)
        requestedVehicle = updateVehicle.newPropulsion(propulsion)
        requestedVehicle = updateVehicle.newRoll(roll)
        requestedVehicle = updateVehicle.newSensorsOk(sensorsOk)
        requestedVehicle = updateVehicle.newSpeed(speed)
        requestedVehicle = updateVehicle.newStageCompleted(stageComplete)
        requestedVehicle = updateVehicle.newStatus(status)
        requestedVehicle = updateVehicle.newYaw(yaw)
        requestedVehicle = updateVehicle.newTimeSinceLastPacket(timeSinceLastPacket)
        requestedVehicle = updateVehicle.newLastPacketTime(lastPacketTime)
        requestedVehicle = updateVehicle.newTime(time)
        requestedVehicle = updateVehicle.newStageName(stageName)
        requestedVehicle = updateVehicle.newMode(mode)
    
        vehicleDatabase.saveData(requestedVehicle, vehicleName)

# TESTING PURPOSE (add new entries to the database)
# updateDatabase.newEntries()
gcsPacket = None
comm_port = "COM7" # can be swapped out for "/dev/ttyUSB0" for serial connection
baud_rate = "9600"
telemetry_data = None

device = DigiMeshDevice(port=comm_port, baud_rate=baud_rate)
device.open()

network = device.get_network()
network.start_discovery_process()

while network.is_discovery_running():
    time.sleep(.01)

devices = {dev.get_node_id():dev._64bit_addr for dev in network.get_devices()}
devices[device.get_node_id()] = device._64bit_addr

print("This device's name: ", device.get_node_id())
print("Discovered ", devices)

geo_bounds = [Geofence(True, [LatLng(1,0),LatLng(0,1),LatLng(-1,0),LatLng(0,-1)])]
geo_bounds.append(Geofence(False, [LatLng(1,1),LatLng(2,1),LatLng(2,-1),LatLng(1,-1)]))

area = SearchArea([LatLng(1,0),LatLng(0,1),LatLng(-1,0),LatLng(0,-1)])

hiker_pos = LatLng(35.083519, -120.534821)

state = 1
stop = False

packet_buffers = {}
packet_counters = {}

def packet_received(packet):
    print('Received packet from ', packet.remote_device.get_node_id())
    global packet_buffers 
    global packet_counters
    global current_state
    global hiker_position

    dev_addr = packet.remote_device.get_64bit_addr()
    data = None

    if dev_addr not in packet_counters or packet_counters[dev_addr] is 0:
        packet_counters[dev_addr] = struct.unpack("I", packet.data[:4])[0] -1 
        data = packet.data[4:]
        print("expecting ", packet_counters[dev_addr]," packets")
        packet_buffers[dev_addr] = b''
    else:
        packet_counters[dev_addr] -= 1
        data = packet.data

    packet_buffers[dev_addr] += data

    if packet_counters[dev_addr] is 0:
        with read_lock: # Acquire lock to read command data from GCS
            telemetry_data = ToGCS.deserialize(packet_buffers[dev_addr])
            gcsPacket = telemetry_data
            #gcsPacket = telemetry_data
            # newEntries()
            print(packet.remote_device.get_node_id(), ": ", telemetry_data)

device.add_data_received_callback(packet_received)

try:
    # dataReceived = XBeeReceiver(9, device)
    # dataReceived.start_decode_thread()
    while True:
        print(type(gcsPacket))
        if gcsPacket is not None:
            print(type(gcsPacket))
            updateDatabase.newEntries()


        cmd = input("Enter command (+,-,s,e,m,b): ")
        if cmd is '+':
            state += 1
            print("New state", state)
        if cmd is '-':
            state -= 1
            print("New state", state)
        if cmd is 's':
            stop = not stop
        if cmd is 'e':
            ToERU(stop, state, hiker_pos, geo_bounds, LatLng(5,5), LatLng(5.5,5.5), False, None, True).serialize().transmit(device, devices['eru'])
        if cmd is 'm':
            ToMAC(None, state, hiker_pos, geo_bounds, [area], LatLng(5,5), LatLng(5.5,5.5), True).serialize().transmit(device, devices['mac'])       
except KeyboardInterrupt:
    print('Stopping')
finally:
   device.del_data_received_callback(packet_received)