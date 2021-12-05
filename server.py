from flask import Flask, jsonify, request
from flask.templating import render_template
import model
import datetime
app = Flask(__name__)

hours ={4: ['Becker House Dining', 'Dining Room', 'Carl Becker House', 'West Campus', '5:00pm - 8:00pm'], 9: ['Cook House Dining', 'Dining Room', 'Alice Cook House', 'West Campus', '5:00pm - 8:00pm'], 17: ['Jansen\'s Dining', 'Dining Room', 'Hans Bethe House', 'West Campus', '4:30pm - 7:30pm'], 19: ['Keeton House Dining', 'Dining Room', 'William Keeton House', 'West Campus', '5:00pm - 8:00pm'], 23: ['North Star', 'Dining Room', 'Appel Commons, Third floor', 'North Campus', '5:00pm - 8:30pm'], 24 : ['Okenshields', 'Dining Room', 'Willard Straight Hall', 'Central Campus', '5:00pm - 8:00pm'], 25: ['Risley House Dining', 'Dining Room', 'Risley Residential College', 'North Campus', '5:00pm - 8:00pm'], 26 : ['RPCC Marketplace', 'Dining Room', 'RPCC, Third floor', 'North Campus', '5:30pm - 8:30pm'], 27: ['Rose House Dining', 'Dining Room', 'Flora Rose House', 'West Campus', '5:00pm - 8:00pm']}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    dateEntry = request.args.get('dateEntry')
    dateEntry = dateEntry.split("/")
    if int(dateEntry[1]) < 10:
        dateEntry[1] = '0' + dateEntry[1]
    if int(dateEntry[0]) < 10:
        dateEntry[0] = '0' + dateEntry[0]
    dayEntry = datetime.date(day=int(dateEntry[1]), month=int(dateEntry[0]), year=int(dateEntry[2])).strftime('%A %d %B %Y').split(" ")[0]
    dateEntry = dateEntry[2]+"-"+dateEntry[0]+"-"+dateEntry[1]
    foods = model.predict_menu(model.getFood(), model.convert_features(dateEntry, dayEntry, int(request.args.get('ID'))))
    return jsonify({'foods': foods, 'hours' : hours[int(request.args.get('ID'))]}) 

if __name__ == '__main__':
   app.run(port = 5000, host="0.0.0.0")