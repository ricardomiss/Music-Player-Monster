import json

def cargarConfig(configFile):
    with open(configFile, "r") as file:
        data = json.load(file)
    return data

def modifConfig(configFile, data):
    with open(configFile, "w") as file:
        json.dump(data, file, indent=4)