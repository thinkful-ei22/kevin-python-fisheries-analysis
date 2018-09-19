import pandas as pd 
from tabulate import tabulate

fishing = pd.read_csv('ICESCatchDataset2006-2016.csv')

pd.set_option('display.max_columns', None)

fishing = fishing[['Species', 'Area', 'Country', 
'2016', '2015', '2014', '2013', '2012', '2011', 
'2010', '2009', '2008', '2007', '2006' ]]

fishing_data = fishing.dropna(axis='rows')
fishing_data = fishing_data[(fishing != 0).all(1)]
fishing_test = fishing_data[8:14]
fishing_test['Depleted'] = pd.Series('No', index=fishing.index)
# values each year are in the units of TLW -- tons of live weight
# species are denoted by an abbreviation ex. ANF

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

# str = input('Enter in the upper limit year')
# print(str)

location(fishing_test)
print(tabulate(fishing_test, headers='keys', tablefmt='grid'))
original_data = len(fishing)
print('There are %d total entries in the 2006-2016 ICES Nominal Catch Dataset' % original_data)
filtered_data = len(fishing_data)
print('%d entries are being analyzed that contain non-zero values.' % filtered_data)

#this discrepancy from 50,000+ to 7000 is likely due to some species of fish and shellfish being naturally rare/scarce in some waters

# do analysis on the years 