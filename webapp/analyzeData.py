import pandas as pd
import json
from flask import jsonify
import getData

def claims_by_field(field, df):
    """
    Determine how many claims were made for each airport, airline, or month
    """
    if field == 'airport':
        s = df['airport_code'].value_counts()
        airports = pd.DataFrame(s).reset_index()
        airports.columns = ['airport_code', 'claims_count']

        return airports

    if field == 'airline':
        s = df['airline_name'].value_counts()
        airlines = pd.DataFrame(s).reset_index()
        airlines.columns = ['airline_name', 'claims_count']

        return airlines

    if field == 'month':
        month_val = df['date_received'].dt.month
        s = month_val.value_counts()

        month_count = pd.DataFrame(s).reset_index()
        month_count.columns = ['month', 'claims_count']

        return month_count

    else:
        print("Please enter one of the following as a field: airport, airline, month")
        raise ValueError

def by_compensation(df):
    """
    Determine which airlines compensate the most
    """
    df = df[df.close_amount != '$0.00 ']
    df = df[df.close_amount != '-']

    airlines = df['airline_name'].value_counts()
    return airlines

def get_airport_data(df):
    """
    Format airport data
    """
    airports = claims_by_field('airport', df)
    airports_bad = airports[0:20]

    chart_data = json.loads(airports_bad.to_json(orient='records'))

    return chart_data

def get_airlines_data(df):
    """
    Format airline data
    """
    airlines = claims_by_field('airline', df)
    airline_bad = airlines[0:20]
    airline_good = airlines.loc[airlines['claims_count'] == 1]

    bad_json = json.loads(airline_bad.to_json(orient='records'))
    good_json = json.loads(airline_good.to_json(orient='records'))

    data = {'bad_airlines': bad_json,
            'good_airlines': good_json}

    return data
