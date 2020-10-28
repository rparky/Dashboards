import pandas as pd

data1 = pd.read_csv('Data/2020_10_13.csv')
data2 = pd.read_csv('Data/2020_10_20.csv')
data = pd.concat([data1, data2], ignore_index=True)
data['EVENTTIME'] = pd.to_datetime(data['EVENTTIME'])
test_to_meta = pd.read_csv('Data/Links/testtotmeta.csv')
joined = data.merge(test_to_meta, left_on='METADATATYPEID', right_on='MetadataTypeId')
joined.to_pickle('Data/combined.pkl')

# add two tests linking the percentage repeats
# create a refined dataset based upon percentage repeats
# create a test comparator using scatter matrix - sort by asset and direction
# create a test reviewer using stripplot sorting by test - this could be linked to event_time graph
# create a parameter section for dealing barrier length etc
# create option to use good or bad dataset
# create option to add lower/upper bands
# ultimately create three pages:
# one for analysing a test in isolation
# one for comparing tests and parameters
# one for view test results in reference to test types
# analyse if passed: start all bad, null = inconclusive, in range = good, iterate through tests
