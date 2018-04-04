import sqlite3
import pandas as pd
from flask import Flask, render_template, jsonify
import analyzeData

app = Flask(__name__)

connection = sqlite3.connect('tsaclaims.db')
# TODO: make into sqlalchemy query
query = "select * from tsa_claims"
df = pd.read_sql(query, connection)

@app.route("/")
def index():
    table = analyzeData.run_ml(df)
    airport_table = table[0][0]
    airline_table = table[1][0]
    d = {'Airport Predictions': [table[0][1], table[0][2]],
         'Airline Predictions': [table[1][1], table[1][2]]}
    results_table = pd.DataFrame(data=d)

    return render_template("index.html", tables=[airport_table.to_html(), airline_table.to_html(), results_table.to_html()],
                           titles=['na', 'Airports', 'Airlines', 'Results'])

@app.route("/data")
def get_data():
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

