from flask import Flask, render_template, request
from database2 import db, get_line_sum
from sqlalchemy.sql import func



app = Flask(__name__)      
 
@app.route('/')
def home():
	return render_template('home.html')


@app.route('/chart', methods=['POST'])
def chart():
	line = int(request.form['line']) 
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
		recovery[i] = int((fare[i] / cost[i]) * 100)
		i += 1
	

	return render_template('chart.html',
		line= line,
		zones= zones,
		fare = fare,
		cost = cost,
		recovery = recovery
		)

if __name__ == '__main__':
  	app.run(debug=True)