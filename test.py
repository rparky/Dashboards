import pandas as pd

data = pd.read_csv('Data/data.csv')
test_to_meta = pd.read_csv('Data/test_to_meta.csv')
refs = pd.read_csv('Data/References.csv')
joined = data.merge(test_to_meta, left_on='METADATATYPEID', right_on='MetadataTypeId')
a = 1
