from datetime import datetime
import json

# updateStage.py handles checking stage id and updating the general stage for frontend

now = datetime.now()

class updateStage():

    # Checks to see if the new entry is newer than the saved entry
    def updateTime(newEntry, newTime):
        # #### Used for resetting updateStage.json ###########################
        # # The default time and stage will be 12 AM and 0 
        # oldTime = now.replace(hour=0, minute=0, second=0, microsecond=0)
        # generalStage = 0

        # # Dictionary format to be saved to JSON File 
        # stageFormat = {
        #     "time": str(oldTime),
        #     "vehicle": "Default",
        #     "general_stage": generalStage,
        #     "stage_name": "Ready to Start"
        # }

        # # Writing dictionary into updateStage.json 
        # jsonFile = open("updateStage.json", "w")
        # json.dump(stageFormat, jsonFile)
        # jsonFile.close()
        # ###################################################################

        # Information from the latest vehicle entry
        vehicleName = newEntry['vehicle_name']
        newStage = newEntry['current_stage']
        stageName = newEntry['stage_name']
        estop = newEntry['estop']

        # Open the updateStage.json and load it 
        jsonFile = open("updateStage.json")
        dataValue = json.load(jsonFile)

        # Declare variable for the stored time and convert from string to time data type
        jsonValue = dataValue['time']
        oldTime = datetime.strptime(jsonValue, '%Y-%m-%d %H:%M:%S.%f')

        #newTime = datetime.strptime(newTime, '%Y-%m-%d %H:%M:%S')

        # Check if newTime is greater and update the JSON File
        if (newTime > oldTime):

            # Dictionary format for the new time and stage
            stageFormat = {
            "time": str(newTime),
            "vehicle": vehicleName,
            "general_stage": newStage,
            "stage_name": stageName,
            "estop": estop
            }

            # print(stageFormat)

            # Write the dictionary to the JSON File
            jsonFile = open("updateStage.json", "w")
            json.dump(stageFormat, jsonFile)
            jsonFile.close()

    def updateStageName(currentStage): 
        stageNames = ["Ready to Start", "Takeoff to Minimum Altitude", "Find the Hiker", "ERU Drop",
                        "ERU Landing Sequence", "Drive to Hiker", "Load the Hiker", "Go to EZ", "Transferring Hiker",
                        "Return to Home/Travel to Position"]
        return stageNames[currentStage]



# # For testing 
# newestPacketTime = now.replace(hour=8, minute=6, second=0, microsecond=0)
# updateStage.updateTime(newestPacketTime, 4)