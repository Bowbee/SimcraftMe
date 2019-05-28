import json
import requests

headers = {'Content-Type': 'application/json'}
serverReturn = requests.post('http://simcraft.me/api/1/sim', headers=headers, data=json.dumps({'region':'us','realm':'frostmourne','character':'bowbi', 'iterations':1000}))
print(serverReturn.json())



reportID = serverReturn.json()['ReportID']



serverReturnStatus = requests.post('http://simcraft.me/api/1/status', headers=headers, data=json.dumps({'reportID':'pCvnTOJs7855Yv2l4pfH'}))

print(serverReturnStatus.json())
