import json
import requests

access_json = 'boxyz_json.json'

#recupere la temperature par defaut
def GetTempDefault():
    with open(access_json, "r") as f:
        Json = json.load(f)
        temp_default = Json["settings"]["heatDefault"]
        return temp_default

#Envoye une request
def post(ip, message):
    try:
        return requests.post(url=ip, data=message)
    except:
        print("Erreur: post failed")

