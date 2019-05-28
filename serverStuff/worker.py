import sqlite3
import os
import subprocess
import time

JOB_STATE_QUEUED = 0
JOB_STATE_RUNNING = 1
JOB_STATE_DONE = 2
JOB_STATE_FAILED = 3

HOMEDIR = "/opt/simcraft.me/"
THREADS = 2

running = True

db_filename = "simcraftmeDB.db"
db = sqlite3.connect(db_filename)

def init_db(): #Initialise the database if the table doesnt exist
	cur = db.cursor()
	cur.execute('''
		CREATE TABLE IF NOT EXISTS simc_jobs 
		(id INTEGER PRIMARY KEY AUTOINCREMENT,
		reportID TEXT,
		status INTEGER DEFAULT 0,
		charRegion TEXT,
		charRealm TEXT,
		charName TEXT,
		numIterations INTEGER,
		fightLen INTEGER,
		enemyCount INTEGER,
		fightStyle INTEGER,
		simString TEXT,
		CONSTRAINT reportID_unique UNIQUE (reportID));
	''')
	db.commit()

def get_next_job(): #get the next job and return the row data
	cur = db.cursor()
	cur.execute("SELECT * FROM simc_jobs WHERE status=? LIMIT 1;", (JOB_STATE_QUEUED,))
	job_data = cur.fetchone()
	if job_data != None:
		cur.execute("UPDATE simc_jobs SET status=? WHERE reportID=?", (JOB_STATE_RUNNING, job_data[1],))
		db.commit()
	return job_data

def run_job(args): #parse data from db_row and run simulation through subprocess, simc exec will output html and xml
	output = ""
	reportID = args[1]
	region = args[3]
	realm = args[4]
	character = args[5]
	iterations = args[6]
	fightLen = args[7]
	enemyCount = args[8]
	fightStyle = args[9]
	simString = args[10]

	print("ARGS:", args)
	print("SIMSTRING:",simString)
	if simString == "" or simString == None:
		print("NO SIM STRING")
		output += "\n armory={},{},{}".format(region,realm,character)

		output += "\niterations={}".format(iterations)
		output += "\nthreads={}".format(THREADS)
		output += "\nmax_time={}".format(fightLen)
		if(enemyCount > 1):
			output += "\nenemy=Patchwerk"
			for i in range(1,enemyCount):
				output += "\nenemy=enemy{}".format(i+1)
		output += "\nfight_style=Patchwerk"
	else:
		output += "{}".format(simString)

	output += "\nhtml={}/reports/{}.html".format(HOMEDIR, reportID)
	output += "\nxml={}/reports/{}.xml".format(HOMEDIR, reportID)
	output += "\noutput={}/reports/{}.txt".format(HOMEDIR, reportID)

	print("OUT:", output)
	
	with open('{}.simc'.format(reportID), 'w') as file:
		file.write(output)
	result = subprocess.run(["./simc/engine/simc", '{}.simc'.format(reportID)], stdout=subprocess.PIPE)
	commandText = result.stdout.decode('UTF-8')
	print(commandText)
	if result.returncode == 0:
		new_state = JOB_STATE_DONE
	if result.returncode == 1:
		new_state = JOB_STATE_FAILED
	cur = db.cursor()
	cur.execute("UPDATE simc_jobs SET status=? WHERE reportID=?", (new_state, reportID,))
	db.commit()
	
	if(os.path.isfile("%s.simc" % reportID)):
		os.remove("%s.simc" % reportID)

def main():
	while running:
		job_data = get_next_job()
		if job_data is not None:
			run_job(job_data)
		else:
			time.sleep(0.5) #if no job is found, sleep for 0.5 seconds


if __name__ == "__main__":
	main()