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

def depletion_breakdown (original, fishing, lower, upper):
  try:
    l_count = 0
    u_count = 0
    for column in fishing:
      # print(column)
      # print(lower == column, lower)
      if lower == column:
        l_count+=1
      else:
        continue

      if l_count == 0: 
        raise KeyError('This is not a valid lower limit Year')

      if upper == column:
        u_count+=1
        break
        return
      else:
        continue
        
      if u_count == 0:
        raise KeyError('This is not a valid upper limit Year')
        return
  except Exception as error: 
    print('Caught this error: ' + repr(error))

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
  
  print(tabulate(fishing_test, headers='keys', tablefmt='grid'))
  original_data = len(original)
  print('There are %d total entries in the 2006-2016 ICES Nominal Catch Dataset.' % original_data, end='\n\n')
  filtered_data = len(fishing_data)
  print('Out of the %d, %d filtered entries are being analyzed that contain non-zero values.' % (original_data, len(fishing_test)), end='\n\n')
  df = fishing['Species'].value_counts()
  unique_species = len(df)
  print('There are %d unique species being caught in the Atlantic Northeast.' % unique_species, end='\n\n')
  depletion_totals = fishing_test['Depleted'].value_counts()
  # print(str)
  depl_yes = depletion_totals['Yes']
  depl_no = depletion_totals['No']
  proportion = depl_yes/(depl_no+depl_yes)
  print('There are %d entries that are classified as depleted and %d entries that are not \n -- a proportion of %.4f' % (depl_yes, depl_no, proportion))
  #this discrepancy from 50,000+ to 7000 is likely due to some species of fish and shellfish being naturally rare/scarce in some waters

# def detailed_species_depletion ():


lower_limit = input('Enter in the lower limit year to analyze:  ')
print(lower_limit)
upper_limit = input('Enter in the upper limit year to analyze:  ')
print(upper_limit)

depletion_breakdown(fishing, fishing_test, lower_limit, upper_limit)


# do analysis on the years 