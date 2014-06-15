from flask import Flask, render_template, request
from database2 import db, get_line_sum
from sqlalchemy.sql import func
import csv


app = Flask(__name__)      
 
@app.route('/')
def home():
	return render_template('home.html')


@app.route('/chart', methods=['POST'])
def chart():
	line = int(request.form['line']) 
	direction = request.form['direction']
	z, f, c = get_line_sum()
	length = len(z)
	zones = range(length)
	fare = range(length)
	cost = range(length)
	recovery = range(length)
	i = 0
	while (i < length):
		zones[i] = z[i]
		fare[i] = f[i]
		cost[i] = c[i]
		if cost[i] == 0:
			recovery[i] = 0
		else:
			recovery[i] = int((fare[i] / cost[i]) * 100)
		i += 1
	''' 
		#section for writing to csv file
		with open('data.csv', 'wb') as csvfile:
	    datawriter = csv.writer(csvfile, delimiter=',',
	                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
	    datawriter.writerow(['Zone'] + ['Fare'] + ['Cost'] + ['Recovery'])
	    data = range(length)
	    while (i < length):
	    	datatable[i] = [zones[i], fare[i], cost[i], recovery[i]]
	    datawriter.writerow(datatable[i])
	    i += 1
	'''

	return render_template('chart.html',
		line= line,
		direction = direction,
		zones= zones,
		fare = fare,
		cost = cost,
		recovery = recovery
		)

if __name__ == '__main__':
  	app.run(debug=True)