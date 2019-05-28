import json
import requests
import time

headers = {'Content-Type': 'application/json'}

def startSim(num):
	serverReturn = requests.post('http://simcraft.me/api/1/sim', headers=headers, data=json.dumps({'region':'us','realm':'frostmourne','character':'bowbi', 'iterations':10000}))
	print("{}. Report ID:".format(num), serverReturn.json()['ReportID'])
	step1 = False
	print("{}. Job Added...".format(num))

	status = getStatus(serverReturn.json()['ReportID'])
	while status == 0 or status == 1:
		status = getStatus(serverReturn.json()['ReportID'])
		if status == 1 and step1 == False:
			print("{}. Processing...".format(num))
			step1 = True
		if status == 2:
			return True
		if status == 3:
			return False

def getStatus(reportID):
	global status
	serverReturn = requests.post('http://simcraft.me/api/1/status', headers=headers, data=json.dumps({'reportID':reportID}))
	return serverReturn.json()['Status'][0]
	time.sleep(0.5)

def run(iterations):
	counter = 1
	target = iterations + 1
	while counter < target:
		ret = startSim(counter)
		if ret:
			print("Sim #{} completed\n".format(counter))
		else:
			print("Sim #{} failed :(\n".format(counter))
		counter += 1

run(1000)