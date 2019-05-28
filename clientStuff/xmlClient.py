import json
import requests
import os


saveDir = "xmlDownloads/"
if not os.path.exists(saveDir):
    os.makedirs(saveDir)

apiURL = 'http://simcraft.me/api/1/xml'
headers = {'Content-Type': 'application/json'}

reportID = 'C048M5WqAvZxWhCrSvXQ'

jsonRequest = {'reportID':reportID}
serverReturn = requests.post(apiURL, headers=headers, data=json.dumps(jsonRequest))
serverReturn.encoding = 'utf-8'
with open(saveDir+reportID+'.xml', 'wb') as file:
	file.write(serverReturn.text.encode("utf-8"))
