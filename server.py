from flask import Flask, jsonify, request
from flask.templating import render_template
import model
import pickle
import datetime
app = Flask(__name__)

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
    foods = model.predict_menu(model.getFood(), model.convert_features(dateEntry, dayEntry))
    print(foods)
    return jsonify({'foods': foods}) 

if __name__ == '__main__':
   app.run(port = 5000, host="0.0.0.0")