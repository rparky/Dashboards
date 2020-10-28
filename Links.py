import pandas as pd

references = pd.read_csv('Data/Links/testtoreference.csv').sort_values('Reference')
thresholds = pd.read_csv('Data/Info/thresholds.csv')

def get_test_refs(chosen_test_type):
    chosen_references = references.loc[references['TestTypeId'] == chosen_test_type].sort_values('Reference')
    return [{'label': row['Reference'], 'value': row['TestId']} for _, row in chosen_references.iterrows()]

def get_thresholds_for_a_test(chosen_test):
    chosen_references = thresholds.loc[thresholds['TestId'] == chosen_test]
    lower, upper = chosen_references['Lower'].iloc[0], chosen_references['Upper'].iloc[0]
    return lower, upper

