import pandas as pd

test = pd.read_csv('Data/Names/test.csv')

channels = {'inclination': [5, 6, 7, 8, 9, 10, 12, 13, 14, 18, 21, 22, 23, 24,
                            25, 26, 27, 112, 113, 114, 115, 126, 128, 146, 149, 150],
            'motor': [28, 100, 101, 102, 103, 104, 105, 120, 134],
            'yellow_lights': [1, 2, 3, 129, 132],
            'red_lights': [1, 4, 14, 15, 125],
            'audible_warning': [3, 11, 16, 130, 131],
            'relays': [4, 5, 8, 9, 11, 12, 112, 114, 115, 125, 128, 133]}


for key, value in channels.items():
    test[key] = False
    test.loc[test['TestId'].isin(value), key] = True

test.to_csv('Data/Info/categories.csv')
a = 1

