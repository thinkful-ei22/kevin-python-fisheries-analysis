import pandas as pd 
from tabulate import tabulate

fishing = pd.read_csv('ICESCatchDataset2006-2016.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

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

def data_analysis (fishing, lower, upper):
  for index, row in fishing.iterrows():
    count = row[2]
    # print(row)
    # print(row['2016'])
    # print(index)
    # print(row[2])
    # print(row[2] < row[12] * .7)
    if row[upper] < row[lower]*.799:
      #.79 value retrieved from Technical Guidance On the Use of Precautionary
      #  Approaches to Implementing National Standard 1 of the
      # Magnuson-Stevens Fishery Conservation and Management Act 1998
      # print('yes')
      fishing.at[index, 'Depleted'] = 'Yes'

lower_limit = input('Enter in the lower limit year to analyze:  ')
print(lower_limit)
upper_limit = input('Enter in the upper limit year to analyze:  ')
print(upper_limit)

data_analysis(fishing_test, lower_limit, upper_limit)
# print(tabulate(fishing_test, headers='keys', tablefmt='grid'))
original_data = len(fishing)
print('There are %d total entries in the 2006-2016 ICES Nominal Catch Dataset' % original_data)
filtered_data = len(fishing_data)
print('Out of the %d, %d filtered entries are being analyzed that contain non-zero values.' % (original_data, filtered_data))
df = fishing['Species'].value_counts()
unique_species = len(df)
print('There are %d unique species being caught in the Atlantic Northeast.' % unique_species)
str = fishing_test['Depleted'].value_counts()
print(str)
proportion = str['Yes']/(str['Yes']+str['No'])
print('There are %d entries that are classified as depleted and %d entries that are not \n -- a proportion of %.4f' % (str['Yes'], str['No'], proportion))
#this discrepancy from 50,000+ to 7000 is likely due to some species of fish and shellfish being naturally rare/scarce in some waters

# do analysis on the years 