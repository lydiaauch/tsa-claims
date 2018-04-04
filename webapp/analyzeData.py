import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing
from sklearn import metrics
import json


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
    airlines = airlines[airlines.airline_name != '-']

    airline_bad = airlines[0:20]
    airline_good = airlines.loc[airlines['claims_count'] == 1]

    bad_json = json.loads(airline_bad.to_json(orient='records'))
    good_json = json.loads(airline_good.to_json(orient='records'))

    data = {'bad_airlines': bad_json,
            'good_airlines': good_json}

    return data

def make_ml_table(df):
    ml_df = df[['airline_name','airport_code', 'claim_type', 'close_amount', 'disposition']]
    ml_df = ml_df.dropna(axis=0, how='any')

    # Drop rows if missing values
    ml_df = ml_df[ml_df.disposition != '-']

    # convert monetary value to number
    ml_df[['close_amount']] = ml_df[['close_amount']].replace('[\$,]', '', regex=True).astype(float)

    return ml_df

def run_ml(df):
    """
    Predict settlement based on airport/airline
    """
    scrubbed = make_ml_table(df)

    # randomly set training/test subsets
    scrubbed['is_train'] = np.random.uniform(0, 1, len(scrubbed)) <= .75
    train, test = scrubbed[scrubbed['is_train'] == True], scrubbed[scrubbed['is_train'] == False]

    airport_pred = airport_ml(test, train, scrubbed)
    airline_pred = airline_ml(test, train, scrubbed)

    return [airport_pred, airline_pred]


def airport_ml(test, train, df):
    """
    Predict settlement based on airport
    """
    forest = RandomForestRegressor(n_jobs=1, n_estimators=70, max_features=0.5)
    le = preprocessing.LabelEncoder()

    le.fit(df['airport_code'])

    train_airports = le.transform(train['airport_code'])
    train_airports = train_airports[:, None]

    test_airports = le.transform(test['airport_code'])
    test_airports = test_airports[:, None]

    forest.fit(train_airports, train['close_amount'])

    predictions = forest.predict(test_airports)

    compare = pd.DataFrame({"predicted": predictions, "actual": test['close_amount']})

    mse = metrics.mean_squared_error(predictions, test['close_amount'])
    r2 = metrics.r2_score(predictions, test['close_amount'])

    MSE = 'MSE: {0:f}'.format(mse)
    R2 = 'RSquared: {0:f}'.format(r2)

    return [compare[0:20], MSE, R2]


def airline_ml(test, train, df):
    """
    Predict settlement based on airport
    """
    forest = RandomForestRegressor(n_jobs=1, n_estimators=70, max_features=0.5)
    le = preprocessing.LabelEncoder()

    le.fit(df['airline_name'])

    train_airports = le.transform(train['airline_name'])
    train_airports = train_airports[:, None]

    test_airports = le.transform(test['airline_name'])
    test_airports = test_airports[:, None]

    forest.fit(train_airports, train['close_amount'])

    predictions = forest.predict(test_airports)

    compare = pd.DataFrame({"predicted": predictions, "actual": test['close_amount']})

    mse = metrics.mean_squared_error(predictions, test['close_amount'])
    r2 = metrics.r2_score(predictions, test['close_amount'])

    MSE = 'MSE: {0:f}'.format(mse)
    R2 = 'RSquared: {0:f}'.format(r2)

    return [compare[0:20], MSE, R2]

