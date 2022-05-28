import json
from tkinter import EW
from vehicleDataFormat import *
from datetime import datetime
from vehicleDatabase import *
from generalStage import *


from digi.xbee.devices import DigiMeshDevice
import xbee
import threading
from updateVehicle import *

import os
import time

#from pymavlink import mavutil
from xbee import TransmitThread, ToMAC, ToERU, ToGCS, Orientation, LatLng, ManualControl, Geofence, SearchArea, read_lock
#import mavlink_msg_MAC

import queue
import struct
import time


now = datetime.now()

class updateDatabase():
    def newEntries (gcsPacket, newestPacketTime, vehicleName):

        newestPacketTime = str(newestPacketTime)

        # Update the vehicle dictionary with given values 
        requestedVehicle = updateVehicle.newAltitude(gcsPacket[0])
        requestedVehicle = updateVehicle.newSpeed(gcsPacket[1])
        requestedVehicle = updateVehicle.newRoll(gcsPacket[2])
        requestedVehicle = updateVehicle.newPitch(gcsPacket[3])
        requestedVehicle = updateVehicle.newYaw(gcsPacket[4])
        requestedVehicle = updateVehicle.newLatitude(gcsPacket[5])
        requestedVehicle = updateVehicle.newLongitude(gcsPacket[6])
        requestedVehicle = updateVehicle.newBattery(gcsPacket[7])
        requestedVehicle = updateVehicle.newSensorsOk(gcsPacket[8])
        requestedVehicle = updateVehicle.newCurrentStage(gcsPacket[9])
        requestedVehicle = updateVehicle.newStageCompleted(gcsPacket[10])
        requestedVehicle = updateVehicle.newHikerPositionLat(gcsPacket[11])
        requestedVehicle = updateVehicle.newHikerPositionLng(gcsPacket[12])
        requestedVehicle = updateVehicle.newStatus(gcsPacket[13])
        requestedVehicle = updateVehicle.newPropulsion(gcsPacket[14])
        requestedVehicle = updateVehicle.newGeofenceCompilant(gcsPacket[15])
        requestedVehicle = updateVehicle.newMode("Manual")
        requestedVehicle = updateVehicle.newTimeSinceLastPacket(50)
        requestedVehicle = updateVehicle.newLastPacketTime(98)
        requestedVehicle = updateVehicle.newTime(newestPacketTime)
        requestedVehicle = updateVehicle.newErrMsg("Overheat")
        #print(gcsPacket)
        currentStage = requestedVehicle['current_stage']
        stageName = updateStage.updateStageName(currentStage)
        requestedVehicle = updateVehicle.newStageName(stageName)

        # print(requestedVehicle)
        vehicleDatabase.saveData(requestedVehicle, vehicleName)


    
class Xbee:
    def xbee_run(xbee_data, send_flag, receive_flag, vehicleName, xbee_send_data, controller_data):
        comm_port = "COM8" # can be swapped out for "/dev/ttyUSB0" for serial connection
        baud_rate = "115200"

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

        global data_queue
        global decode_queue 
        data_queue = queue.Queue(9)  
        decode_queue = queue.Queue(9)

        def receive_packets(packet):
            global packet_counter
            global packet_buffer
            packet_buffer = {}
            packet_counter = {}
            '''Used to preprocess packets received from GCS and put them into a queue to await deserialization.
                Since one message from GCS may exceed the maximum packet length, multiple packets may be used to
                send over one message. The preprocessing done by this function collects all those packets up into
                one byte array, where it is then saved in data_queue as one complete message.'''

            if len(packet_counter) == 0:
                # Upon having received all packets, prepare the packet buffer to be stored in data_queue
                packet_counter = struct.unpack("I", packet.data[:4])[0] -1 
                data = packet.data[4:]
                packet_buffer = b''
            else:
                # The entire series of packets containing the message has yet to be fully preprocessed,
                # so put this packet's data into the buffer and go to the next packet
                packet_counter -= 1
                data = packet.data
        
            packet_buffer += data
            #print(self.packet_buffer)
            #print("this is from the packet buffer")
            # Upon having received all packets and the buffer has been prepared, store the data in the queue to
            # await deserialization
            if packet_counter == 0:
                #print("data queue")
                #print(len(self.packet_buffer))
                with read_lock:
                    data_queue.put(packet_buffer)
                    packet_buffer = []

        device.add_data_received_callback(receive_packets)

        TIMEOUT = 1000
        while True:
            if send_flag.value == 1:
                print("Hi")
                send_flag.value = 0
                state = 1
                stop = False
                cmd = ""
                sent = False
                if (vehicleName.value == "ERU"):
                    cmd = "e"
                if (vehicleName.value == "MAC"):
                    cmd = "m"
                # if (vehicleName.value == "MEA"):
                #     cmd = "l"
                #elif (vehicleName.value == "MAC"):
                #    cmd = "m"
                try:
                    if cmd is "s":
                        stop = not stop
                    if cmd is "e":
                        print("Sending to ERU")
                        xbee.read_lock.acquire()
                        ToERU(stop, state, hiker_pos, geo_bounds, LatLng(5,5), LatLng(5.5,5.5), False, 
                            ManualControl(controller_data[0], controller_data[1], controller_data[2], 
                                            controller_data[3], controller_data[4], controller_data[5], 
                                            controller_data[6], controller_data[7]), True, True
                            ).serialize().transmit(device, devices['eru'])
                        xbee.read_lock.release()
                    if cmd is "m":
                        print("Sending to MAC")
                        #device.del_data_received_callback(getPacket.packet_received)
                        ToMAC(None, state, hiker_pos, geo_bounds, [area], LatLng(5,5), LatLng(5.5,5.5), True
                            ).serialize().transmit(device, devices['mac'])
                    # if cmd is "l":
                    #     print("Sending to MEA")
                    #     #device.del_data_received_callback(getPacket.packet_received)
                    #     ToMEA(None, state, geo_bounds, LatLng(5,5), LatLng(5.5,5.5), False, True
                    #         ).serialize().transmit(device, devices['mea'])
                        #sent = True       
                except KeyboardInterrupt:
                    f = 0
                    #device.del_data_received_callback(getPacket.packet_received)
                current_time = int(round(time.time() * 1000))
                xbee_end_time = current_time
                xbee_start_time = current_time
                while (xbee_end_time - xbee_start_time < TIMEOUT):
                    xbee_end_time = int(round(time.time() * 1000))
                    try:
                        data = data_queue.get_nowait()
                        if type(data) == bytes:
                            receive_flag.value = 1
                            decode_queue.put(ToGCS.deserialize(data))
                            xbee_data_temp = decode_queue.get_nowait()
                            xbee_data[0] = xbee_data_temp.altitude
                            xbee_data[1] = xbee_data_temp.speed
                            xbee_data[2] = xbee_data_temp.orientation.roll
                            xbee_data[3] = xbee_data_temp.orientation.pitch
                            xbee_data[4] = xbee_data_temp.orientation.yaw
                            xbee_data[5] = xbee_data_temp.gps.lat
                            xbee_data[6] = xbee_data_temp.gps.lng
                            xbee_data[7] = xbee_data_temp.battery
                            xbee_data[8] = xbee_data_temp.sensors_ok
                            xbee_data[9] = xbee_data_temp.current_state
                            xbee_data[10] = xbee_data_temp.state_complete
                            xbee_data[11] = xbee_data_temp.hiker_position.lat
                            xbee_data[12] = xbee_data_temp.hiker_position.lng
                            xbee_data[13] = xbee_data_temp.status
                            xbee_data[14] = xbee_data_temp.propulsion
                            xbee_data[15] = xbee_data_temp.geofence_compliant
                            xbee_data[16] = xbee_data_temp.manual_mode
                            TIMEOUT = 1000
                            break
                            #print(xbee_data_temp)

                            #print(self.decode_queue.qsize())
                    except queue.Empty:
                        TIMEOUT = 1000
                        # print("hi")
                        # If the packet buffer is empty, do nothing
                        # The TransmitThread object will call this function in the next iteration of its loop,
                        # so nothing is done here to simply let the thread check again