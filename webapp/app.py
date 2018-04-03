import sqlite3
import pandas as pd
import json
from flask import Flask, render_template, jsonify
import makeVis
import analyzeData

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    connection = sqlite3.connect('tsaclaims.db')
    # TODO: make into sqlalchemy query
    query = "select * from tsa_claims"

    df = pd.read_sql(query, connection)

    airlines_data = analyzeData.get_airlines_data(df)
    airport_data = analyzeData.get_airport_data(df)

    data = {'vis_data': {
                "airport_data" : airport_data,
                "airline_data" : airlines_data
            }}

    return jsonify(data)

@app.route('/about')
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost')

