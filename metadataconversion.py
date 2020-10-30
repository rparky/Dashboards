import pandas as pd

data = pd.read_csv('Data/Names/metadatatypes.csv')

# Get rid of non LX stuff
data = data.loc[data['METADATATYPEID'] > 32]
data = data.loc[~data['METADATATYPEID'].between(126, 138)]

# use metadatavalue names to get name and location
names = data['VALUE'].copy().values
location = [""] * len(names)
corners = ['(AUX) ', 'YN ', 'YO ', 'ZN ', 'ZO ', 'Yn ', 'Yo ', 'Zn ', 'Zo ']
other = ["1", "2", "(Left) ", "(Right) "]
for i in range(len(names)):
    for corner in corners:
        if corner in names[i]:
            location[i] = location[i] + corner
        names[i] = names[i].replace(corner, "")
    for word in other:
        names[i] = names[i].replace(word, "")
    names[i] = names[i].replace("Light ", "Lights ")
    if location[i] == "":
        location[i] = "N/A"

location = [loc.strip().replace('(AUX)', 'Aux') for loc in location]

data['Test Names'] = names
data['TestSubRef'] = location

# add reliability info
for i, corner in zip([2000, 2001, 2002, 2003], ['YN', 'YO', 'ZN', 'ZO']):
    data.loc[i, 'METADATATYPEID'] = i
    data.loc[i, 'Test Names'] = 'Longest repeat'
    data.loc[i, 'TestSubRef'] = corner

for i, corner in zip([2004, 2005, 2006, 2007], ['YN', 'YO', 'ZN', 'ZO']):
    data.loc[i, 'METADATATYPEID'] = i
    data.loc[i, 'Test Names'] = 'Percentage repeats'
    data.loc[i, 'TestSubRef'] = corner

# find existing testIds
test_id = pd.read_csv('Data/Links/test_meta.csv')
merged = data.merge(test_id, how='left', left_on='METADATATYPEID', right_on='MetadataTypeId', suffixes=[None, '_y'])

# fill in gaps with arbitrary test values
test_names = merged['Test Names'].unique()

for i, name in enumerate(test_names):
    chosen_test = merged.loc[merged['Test Names'] == name]
    if chosen_test['TestId'].isnull().all():
        merged.loc[chosen_test.index, 'TestId'] = 100 + i

merged = merged.sort_values('Test Names').reset_index()

# select relevant info and copy to file
test_names = merged[['TestId', 'Test Names']].copy().drop_duplicates().dropna().sort_values('TestId')
test_to_meta = merged[['TestId', 'TestSubRef', 'METADATATYPEID']].dropna().sort_values('TestId')
test_names.to_csv('Data/Names/test.csv')
test_to_meta.to_csv('Data/Links/test_meta2.csv')
a = 1
