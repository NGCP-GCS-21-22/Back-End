import json
from tkinter import EW
from vehicleDataFormat import *
from datetime import datetime
from vehicleDatabase import *
from generalStage import *

from queue import Empty
import time
from digi.xbee.devices import DigiMeshDevice
import xbee
from xbee import TransmitThread, read_lock, ToERU, ToMAC, ToGCS, Orientation, LatLng, ManualControl, Geofence, SearchArea
import threading
import struct
from updateVehicle import *

now = datetime.now()

class updateDatabase():
    def newEntries (gcsPacket, newestPacketTime):

        newestPacketTime = str(newestPacketTime)

        # Update the vehicle dictionary with given values 
        requestedVehicle = updateVehicle.newAltitude(gcsPacket.altitude)
        requestedVehicle = updateVehicle.newBattery(gcsPacket.battery)
        requestedVehicle = updateVehicle.newCurrentStage(gcsPacket.current_state)
        requestedVehicle = updateVehicle.newGeofenceCompilant(gcsPacket.geofence_compliant)
        requestedVehicle = updateVehicle.newLatitude(gcsPacket.gps.lat)
        requestedVehicle = updateVehicle.newLongitude(gcsPacket.gps.lng)
        requestedVehicle = updateVehicle.newPitch(gcsPacket.orientation.pitch)
        requestedVehicle = updateVehicle.newPropulsion(gcsPacket.propulsion)
        requestedVehicle = updateVehicle.newRoll(gcsPacket.orientation.roll)
        requestedVehicle = updateVehicle.newSensorsOk(gcsPacket.sensors_ok)
        requestedVehicle = updateVehicle.newSpeed(gcsPacket.speed)
        requestedVehicle = updateVehicle.newStageCompleted(gcsPacket.state_complete)
        requestedVehicle = updateVehicle.newStatus(gcsPacket.status)
        requestedVehicle = updateVehicle.newYaw(gcsPacket.orientation.yaw)
        requestedVehicle = updateVehicle.newTimeSinceLastPacket(50)
        requestedVehicle = updateVehicle.newLastPacketTime(98)
        requestedVehicle = updateVehicle.newTime(newestPacketTime)
        requestedVehicle = updateVehicle.newMode("Manual")
        requestedVehicle = updateVehicle.newHikerPositionLat(gcsPacket.hiker_position.lat)
        requestedVehicle = updateVehicle.newHikerPositionLng(gcsPacket.hiker_position.lng)
        requestedVehicle = updateVehicle.newErrMsg("Overheat")

        currentStage = requestedVehicle['current_stage']
        stageName = updateStage.updateStageName(currentStage)
        requestedVehicle = updateVehicle.newStageName(stageName)

        # print(requestedVehicle)
        vehicleDatabase.saveData(requestedVehicle, "MAC")


comm_port = "COM7" # can be swapped out for "/dev/ttyUSB0" for serial connection
baud_rate = "9600"
telemetry_data = ""

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

class getPacket():
    
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
            with xbee.read_lock: # Acquire lock to read command data from GCS
                telemetry_data = ToGCS.deserialize(packet_buffers[dev_addr])
                newestPacketTime = now.strftime("%H:%M:%S")
                updateDatabase.newEntries(telemetry_data, newestPacketTime)
                #gcsPacket = telemetry_data
                # print(packet.remote_device.get_node_id(), ": ", telemetry_data)


    def start_receiving():
        device.add_data_received_callback(getPacket.packet_received)

    #def stop_receiving():
    #    device.del_data_received_callback(getPacket.packet_received)

    def getName(vehicleName):
        state = 1
        cmd = ""
        sent = False
        if (vehicleName == "MAC"):
            cmd = "m"
        if (vehicleName == "ERU"):
            cmd = "e"
        try:
            # while True:
            if cmd is "+":
                state += 1
                print("New state", state)
            if cmd is "-":
                state -= 1
                print("New state", state)
            if cmd is "s":
                stop = not stop
            if cmd is "e":
                ToERU(stop, state, hiker_pos, geo_bounds, LatLng(5,5), LatLng(5.5,5.5), False, None, True).serialize().transmit(device, devices['eru'])
            if cmd is "m":
                #device.del_data_received_callback(getPacket.packet_received)
                with xbee.read_lock:
                    ToMAC(None, state, hiker_pos, geo_bounds, [area], LatLng(5,5), LatLng(5.5,5.5), True).serialize().transmit(device, devices['mac'])
                #sent = True       
        except KeyboardInterrupt:
            #device.del_data_received_callback(getPacket.packet_received)
            pass
        finally:
            pass
