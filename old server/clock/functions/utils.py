import json

access_json = 'boxyz_json.json'

#recupere la temperature par defaut
def GetTempDefault():
    with open(access_json, "r") as f:
        Json = json.load(f)
        temp_default = Json["settings"]["tempDefault"]
        return temp_default