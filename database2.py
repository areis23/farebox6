from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import csv
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'
db = SQLAlchemy(app)


class Output(db.Model):
	__tablename__ = 'output'

	ID = db.Column(db.Integer, primary_key=True)
	LINE_NUMBER = db.Column(db.Integer)
	ZONE_NUMBER = db.Column(db.Integer)
	TIME_RANGE = db.Column(db.String(20))
	DIRECTION = db.Column(db.String(8))
	SCHEDULED_RUN_TIME = db.Column(db.Integer)
	TOTAL_OPERATING_COST = db.Column(db.Float)
	FARE_COLLECTED = db.Column(db.Float)
	FAREBOX_RECOVERY = db.Column(db.Float)
	DATE_STORED = db.Column(db.String(20))
	PCNAME = db.Column(db.String(10))
	SIGN_ON_DATE = db.Column(db.String(20))
	OPERATING_COST_PER_HOUR = db.Column(db.Float)
	RECOVERY_PROCESSING_ID = db.Column(db.Integer)
	AGGREGATE_ID = db.Column(db.Integer)
	COUNTY = db.Column(db.String(20))
	TYPE = db.Column(db.String(10))

	def __init__(self, ID, LINE_NUMBER, ZONE_NUMBER, \
		TIME_RANGE, DIRECTION, SCHEDULED_RUN_TIME, TOTAL_OPERATING_COST, \
		FARE_COLLECTED, FAREBOX_RECOVERY, DATE_STORED, PCNAME, SIGN_ON_DATE, \
		OPERATING_COST_PER_HOUR, RECOVERY_PROCESSING_ID, AGGREGATE_ID, COUNTY, TYPE):
		self.ID = ID
		self.LINE_NUMBER = LINE_NUMBER
		self.ZONE_NUMBER = ZONE_NUMBER
		self.TIME_RANGE = TIME_RANGE
		self.DIRECTION = DIRECTION
		self.SCHEDULED_RUN_TIME = SCHEDULED_RUN_TIME
		self.TOTAL_OPERATING_COST = TOTAL_OPERATING_COST
		self.FARE_COLLECTED = FARE_COLLECTED
		self.FAREBOX_RECOVERY = FAREBOX_RECOVERY
		self.DATE_STORED = DATE_STORED
		self.PCNAME = PCNAME
		self.SIGN_ON_DATE = SIGN_ON_DATE
		self.OPERATING_COST_PER_HOUR = OPERATING_COST_PER_HOUR
		self.RECOVERY_PROCESSING_ID = RECOVERY_PROCESSING_ID
		self.AGGREGATE_ID = AGGREGATE_ID
		self.COUNTY = COUNTY
		self.TYPE = TYPE
def init_db():
	db.create_all()
	with open('Temp2.txt', 'rb') as csvfile:
		fb_reader = csv.DictReader(csvfile, delimiter=',')
		for row in fb_reader:
			db.session.add(Output(row['ID'], row['LINE_NUMBER'], row['ZONE_NUMBER'], \
			row['TIME_RANGE'], row['DIRECTION'], row['SCHEDULED_RUN_TIME'], \
			row['TOTAL_OPERATING_COST'], row['FARE_COLLECTED'], \
			row['FAREBOX_RECOVERY'], row['DATE_STORED'], row['PCNAME'], \
			row['SIGN_ON_DATE'], row['OPERATING_COST_PER_HOUR'], \
			row['RECOVERY_PROCESSING_ID'], row['AGGREGATE_ID'], row['COUNTY'], \
			row['TYPE']))
	db.session.commit()


def get_line_sum():
	line = int(request.form['line'])
	chosen_direction = request.form['direction']
	if chosen_direction in ['Inbound','Outbound']:
		for result in db.session.query(func.count(Output.ZONE_NUMBER.distinct())).filter_by(LINE_NUMBER = line, DIRECTION = chosen_direction):
			length = result[0]
			zones, fare, cost = initialize_variables(length)
		i = 0
		while (i < length):
			zones[i] =  db.session.query(Output.ZONE_NUMBER.distinct()).filter_by(LINE_NUMBER = line, DIRECTION = chosen_direction)[i][0]
			for fare_sum in db.session.query(func.sum(Output.FARE_COLLECTED)).filter_by(LINE_NUMBER = line, ZONE_NUMBER = zones[i], DIRECTION = chosen_direction):
				fare[i] = fare_sum[0]
			for cost_sum in db.session.query(func.sum(Output.TOTAL_OPERATING_COST)).filter_by(LINE_NUMBER = line, ZONE_NUMBER = zones[i], DIRECTION = chosen_direction):
				cost[i] = cost_sum[0]
			i += 1
		return zones, fare, cost
	else:
		for result in db.session.query(func.count(Output.ZONE_NUMBER.distinct())).filter_by(LINE_NUMBER = line):
			length = result[0]
			zones, fare, cost = initialize_variables(length)
		i = 0
		while (i < length):
			zones[i] =  db.session.query(Output.ZONE_NUMBER.distinct()).filter_by(LINE_NUMBER = line)[i][0]
			for fare_sum in db.session.query(func.sum(Output.FARE_COLLECTED)).filter_by(LINE_NUMBER = line, ZONE_NUMBER = zones[i]):
				fare[i] = fare_sum[0]
			for cost_sum in db.session.query(func.sum(Output.TOTAL_OPERATING_COST)).filter_by(LINE_NUMBER = line, ZONE_NUMBER = zones[i]):
				cost[i] = cost_sum[0]
			i += 1
		return zones, fare, cost

def initialize_variables(length):
	zones = range(length)
	fare = range(length)
	cost = range(length)
	return zones, fare, cost
	'''
	for result in db.session.query(func.sum(Output.FARE_COLLECTED)).filter_by(LINE_NUMBER = int(request.form['line']), DIRECTION = chosen_direction, COUNTY = chosen_county):
	line_sum= result[0]
	
	
	if chosen_direction in ['INBOUND', 'OUTBOUND'] and chosen_county in county_list:
		for result in db.session.query(func.sum(Output.FARE_COLLECTED)).filter_by(LINE_NUMBER = int(request.form['line']), DIRECTION = chosen_direction, COUNTY = chosen_county):
			line_sum= result[0]
		for result in db.session.query(func.sum(Output.TOTAL_OPERATING_COST)).filter_by(LINE_NUMBER = int(request.form['line']), DIRECTION = chosen_direction, COUNTY = chosen_county):
			line_cost= result[0]
	elif chosen_direction in ['INBOUND', 'OUTBOUND']:
		for result in db.session.query(func.sum(Output.FARE_COLLECTED)).filter_by(LINE_NUMBER = int(request.form['line']), DIRECTION = chosen_direction):
			line_sum= result[0]
		for result in db.session.query(func.sum(Output.TOTAL_OPERATING_COST)).filter_by(LINE_NUMBER = int(request.form['line']), DIRECTION = chosen_direction):
			line_cost= result[0]	
	elif chosen_county in county_list:	
		for result in db.session.query(func.sum(Output.FARE_COLLECTED)).filter_by(LINE_NUMBER = int(request.form['line']), COUNTY = chosen_county):
			line_sum= result[0]
		for result in db.session.query(func.sum(Output.TOTAL_OPERATING_COST)).filter_by(LINE_NUMBER = int(request.form['line']), COUNTY = chosen_county):
			line_cost= result[0]
	else: 
		for result in db.session.query(func.sum(Output.FARE_COLLECTED)).filter_by(LINE_NUMBER = int(request.form['line'])):
			line_sum= result[0]
		for result in db.session.query(func.sum(Output.TOTAL_OPERATING_COST)).filter_by(LINE_NUMBER = int(request.form['line'])):
			line_cost= result[0]
	return line_sum, line_cost
'''

'''
	def __repr__(self):
		return '<Output %r>' % self.ID
'''

if __name__=="__main__":
	init_db()
	# check to make sure databsae is initialized
	line_query = db.session.query(func.sum(Output.FARE_COLLECTED)).filter_by(LINE_NUMBER = 1)
'''
	for result in line_query:
		line_sum = result[0]
	print line_sum
	'''