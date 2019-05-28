import os
import random
import string
from flask import *
import sqlite3

app = Flask(__name__)
IDLength = 10
homeDir = "/opt/simcraft.me"
JOB_STATE_QUEUED = 0

storage = {}

@app.route('/favicon.ico') #icon
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
						  'favicon.ico',mimetype='image/vnd.microsoft.icon')
@app.route('/') # index.html serve
def index():
	return render_template('index.html')

@app.route('/failed') #failed.html serve
def page_not_found2():
	return render_template('failed.html')

@app.errorhandler(404) #404 error handler, serve custom 404 page
def page_not_found(e):
	return render_template('404.html'), 404
	
@app.errorhandler(401) #401 error handler, serve custom 401 page
def not_auth(e):
	return render_template('401.html'), 401

@app.route('/api/1/sim', methods = ['POST']) #API handler for SIM
def postJSONHandler():
	if(request.is_json):
		reportID = generateID()
		result = validateJSON(request.get_json())
		addJob(reportID, result[0],result[1],result[2],result[3],result[4],result[5],result[6], result[7])
		return json.dumps({'ReportID': reportID})
	else:
		return '404 No JSON'

@app.route('/api/1/advanced', methods = ['POST']) #API handler for SIM (advanced, this is duplicate but still need returns and routes for Flask app)
def postJSONHandlerAdvanced():
	if(request.is_json):
		reportID = generateID()
		result = validateJSON(request.get_json())
		addJob(reportID, result[0],result[1],result[2],result[3],result[4],result[5],result[6], result[7])
		return json.dumps({'ReportID': reportID})
	else:
		return '404 No JSON'

def get_job_status(report_id): #query database for current status
	cur = db.cursor()
	print(report_id)
	cur.execute("SELECT status FROM simc_jobs WHERE reportID=? LIMIT 1;", (report_id,))
	status = cur.fetchone()
	return status

@app.route('/api/1/status', methods = ['POST']) #API Handler for STATUS (calls get_job_status(report_id))
def statusCheck():
	if(request.is_json):
		content = request.get_json()
		print(content)
		reportID = content['reportID']
		status = get_job_status(reportID)
		if status == 2:
			return json.dumps({'Status':status,'URL':'http://simcraft.me/report/%s' % reportID})
		return json.dumps({'Status':status})

@app.route('/api/1/xml',methods = ['POST']) #API Handler for XML (looks for reportID.xml in directory, returns as datastream)
def fetchXML():
	if(request.is_json):
		content = request.get_json()
		if content['reportID']:
			return send_from_directory('reports',content['reportID']+'.xml')
	
@app.route('/report/<reportID>') #Serve reportID if found, otherwise 404
def report(reportID):
	return send_from_directory('reports', reportID+'.html')

@app.route('/simple') # serve simple.html webpage
def simpleSim():
	return render_template('simple.html')

@app.route('/advanced') # serve advanced.html webpage
def advancedSim():
	return render_template('advanced.html')

@app.route('/sim', methods = ['POST']) #old method of posting data to SIM (doesnt work, is not called, including for evidence of design modifications :)
def sim():
	if request.method == 'POST':
		reportID = generateID()
		result = validateJSON(request.form)
		addJob(reportID, result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7])
		return json.dumps({'ReportID': reportID})
		#return redirect(url_for('report', reportID=reportID))
	else:
		return redirect(url_for('index'))

def validateJSON(content): # validate JSON and sanitize input
	region = "us"
	realm = ""
	character = ""
	iterations = 4000
	fightLen = 300
	enemyCount = 1
	fightStyle = 0
	simString = ""

	try:
		region = content['region']
	except:
		pass
	try:
		realm = content['realm']
	except:
		pass
	try:
		character = content['character']
	except:
		pass
	try:
		iterations = int(content['iterations'])
	except:
		pass
	try:
		fightLen = int(content['fightLen'])
	except:
		pass
	try:
		enemyCount = int(content['enemyCount'])
	except:
		pass
	try:
		fightStyle = int(content['fightStyle'])
	except:
		pass
	try:
		simString = content['simString']
	except:
		pass

	result = [region, realm, character, iterations, fightLen, enemyCount, fightStyle, simString]
	print("RESULTS:",result)
	return result

def generateID(): #generate a unique reportID, return it
	return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(20))

def init_db(): # init database if table doesnt exist
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

def addJob(report_id, char_region, char_realm, char_name, num_iterations, fight_len, enemy_count, fight_style, sim_string):
	cur = db.cursor()  #add Job to database when called
	cur.execute('''
		INSERT INTO simc_jobs 
		(reportID,
		status,
		charRegion,
		charRealm,
		charName,
		numIterations,
		fightLen,
		enemyCount,
		fightStyle,
		simString)
		VALUES 
		(?,?,?,?,?,?,?,?,?,?);
		''',
		(report_id,
		JOB_STATE_QUEUED,
		char_region, 
		char_realm, 
		char_name, 
		num_iterations, 
		fight_len, 
		enemy_count, 
		fight_style,
		sim_string)
	)
	db.commit()

#command line params but inline, such as app.run()
db_filename = "simcraftmeDB.db"
db = sqlite3.connect(db_filename, check_same_thread=False)
init_db()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.run(host="0.0.0.0", port=int("80"), debug=False)

