import pandas as pd

refs = pd.read_csv('Data/References.csv')
data = pd.read_pickle('Data/combined.pkl')


def get_test_refs(chosen_test_type):
    references = refs.loc[refs['TestTypeId'] == chosen_test_type]
    references = references.sort_values('Reference')
    return [{'label': row['Reference'], 'value': row['TestId']} for _, row in references.iterrows()]


def get_test_types():
    references = refs['TestTypeId'].unique()
    references.sort()
    return [{'label': i, 'value': i} for i in references]


def get_assets():
    assets = data['ASSETID'].unique()
    assets.sort()
    return [{'label': i, 'value': i} for i in assets]


def get_geographical_area():
    assets = data['ASSETID'].unique()
    assets.sort()
    return [{'label': i, 'value': i} for i in assets]


def get_tests():
    assets = data['ASSETID'].unique()
    assets.sort()
    return [{'label': i, 'value': i} for i in assets]

def get_direction():
    directions = refs['DirectionId'].unique()
    directions.sort()
    return [{'label': i, 'value': i} for i in directions]