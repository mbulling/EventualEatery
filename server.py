from flask import Flask, jsonify, request
from flask.templating import render_template
import pickle
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict')
def predict():
    dateEntry = request.args.get('dateEntry')
    dayEntry = request.args.get('dayEntry')
    return jsonify({'dateEntry': dateEntry, 'dayEntry' : dayEntry}) 

if __name__ == '__main__':
   app.run()