import pandas as pd 
from tabulate import tabulate

fishing = pd.read_csv('ICESCatchDataset2006-2016.csv')

pd.set_option('display.max_columns', None)

fishing = fishing[['Species', 'Area', 'Country', 
'2016', '2015', '2014', '2013', '2012', '2011', 
'2010', '2009', '2008', '2007', '2006' ]]

fishing = fishing.dropna(axis='rows')
fishing_data = fishing[(fishing != 0).all(1)]
fishing_test = fishing_data[8:14]
fishing_test['Depleted'] = pd.Series('No', index=fishing.index)

# fishing_two = fishing_two[0:18]
# fishing=fishing.replace(nan,0)
# del fishing['Unnamed: 15', 'Unnamed: 16']
# print(fishing[['Unnamed: 23']])
# print(tabulate(fishing_two, headers='keys', tablefmt='grid'))

def location (fishing):
  for index, row in fishing.iterrows():
    count = row[2]
    # print(row)
    # print(row['2016'])
    # print(index)
    # print(row[2])
    # print(row[2] < row[12] * .7)
    if row[3] < row[13]*.7:
      # print('yes')
      fishing.at[index, 'Depleted'] = 'Yes'


location(fishing_test)
print(tabulate(fishing_test, headers='keys', tablefmt='grid'))
print(len(fishing_data))
print(len(fishing))

# do analysis on the years 