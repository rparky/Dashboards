import pandas as pd

data = pd.read_pickle('Data/combined.pkl')
filters = ['ASSETID', 'TestSubRef', 'EVENTTIME']
quality = data.loc[(data['TestId'] == 150) & (data['DATAVALUE'] < 60)]
good_list = quality.groupby(filters).count().reset_index()[filters]

cats = pd.read_csv('Data/Info/categories.csv')
good1 = data.loc[data['TestId'].isin(cats.loc[~cats['inclination'], 'TestId'])]
pg = data.loc[data['TestId'].isin(cats.loc[cats['inclination'], 'TestId'])]
good2 = pg.merge(good_list, left_on=filters, right_on=filters)
good = pd.concat([good1, good2], ignore_index=True)
good.to_pickle('Data/good.pkl')
a = 1