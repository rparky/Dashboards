import pandas as pd

assets = pd.read_csv('Data/Names/assets.csv').sort_values('VALUE')
assets_dict = [{'label': row['VALUE'], 'value': row['ASSETID']} for _, row in assets.iterrows()]

test_types = pd.read_csv('Data/Names/testtypes.csv').sort_values('Name')
test_types_dict = [{'label': row['Name'], 'value': row['TestTypeId']} for _, row in test_types.iterrows()]
