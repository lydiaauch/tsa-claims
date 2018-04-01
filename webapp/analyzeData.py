import pandas as pd
import getData

def claims_by_field(field, df):
    """
    Determine how many claims were made for each airport, airline, or month
    """
    if field == 'airport':
        airports = df['airport_code'].value_counts()
        return airports

    if field == 'airline':
        airlines = df['airline_name'].value_counts()
        return airlines

    if field == 'month':
        month_val = df['date_received'].dt.month
        month_count = month_val.value_counts()
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

# Example for using lambda to add new field to dataset
# def get_age_segment(age):
#     if age <= 22:
#         return '22-'
#     elif age <= 26:
#         return '23-26'
#     elif age <= 28:
#         return '27-28'
#     elif age <= 32:
#         return '29-32'
#     elif age <= 38:
#         return '33-38'
#     else:
#         return '39+'
#
# df['age_segment'] = df['age'].apply(lambda age: get_age_segment(age))


if __name__ == '__main__':
    df = getData.get_df()
    scrubbed = getData.scrub_data(df)

    # months = claims_by_field('month', df)
    # airlines = claims_by_field('airline', df)
    # airports = claims_by_field('airport', df)

    comp = by_compensation(scrubbed)
    print(comp)

