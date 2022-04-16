import json

# Mission.py handles saving a new misson from frontened 

class Mission():
    
    # Saves the new mission to a JSON File 
    def createMission(newEntry):
        jsonFile = open("newMission.json", "w")
        json.dump(newEntry, jsonFile)
        jsonFile.close()