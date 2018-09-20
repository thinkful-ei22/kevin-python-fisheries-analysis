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
fishing_test.insert(len(fishing_test.columns), 'Depleted', 'No')
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
  print('There are %d unique species being caught in the Atlantic Northeast based on the year range.' % unique_species, end='\n\n')
  depletion_totals = fishing_test['Depleted'].value_counts()
  depl_yes = depletion_totals['Yes']
  depl_no = depletion_totals['No']
  proportion = depl_yes/(depl_no+depl_yes)
  percentage = proportion*100
  print('There are %d entries that are classified as depleted and %d entries that are not'  % (depl_yes, depl_no))
  print('-- a proportion of %.4f or %.2f%% based on a TAC value of 0.80 - Total Allowable Catch - to maintain sustainability.' % (proportion, percentage))
  print('----------------------------------------------------------------------------', end='\n\n')
  main_function()
  #this discrepancy from 50,000+ to 7000 is likely due to some species of fish and shellfish being naturally rare/scarce in some waters

# def detailed_species_depletion ():

def sum_annual_tlw (fishing, column):
  # console_break = print('----------------------------------------------------------------------------', end='\n\n')
  #add error handling
  tlw_annual = fishing[column].sum()
  column = int(column)
  print('----------------------------------------------------------------------------', end='\n\n')
  print('In %d, there was a total of %.2f TLW (tons live weight) fish and shellfish caught.' % (column, tlw_annual), end='\n\n')
  print('----------------------------------------------------------------------------', end='\n\n')
  main_function()

# lower_limit = input('Enter in the lower limit year to analyze:  ')
# print(lower_limit)
# upper_limit = input('Enter in the upper limit year to analyze:  ')
# print(upper_limit)

# depletion_breakdown(fishing, fishing_test, lower_limit, upper_limit)

# enter_year = input('Enter in a year to sum up:  ')
# print(enter_year)

# sum_annual_tlw(fishing_test, enter_year)

def main_function ():
  print('Available Functions:', end='\n\n')
  print('Numerical Analysis:', end='\n\n')
  print('Enter 1 to Determine Total Annual Catch for a Year', end='\n\n')
  print('Enter 2 to Determine Total Annual Catch for a Range of Years', end='\n\n')
  print('Enter 3 to do Quantitative Analysis of the Health of Fishery Stocks', end='\n\n')
  print('Graphical Representation:', end='\n\n')
  print('Pie Chart', end='\n\n')
  
  option = input('Enter in an option to run an analytical function (or 0 to exit):  ')
  option = int(option)
  # print(option)
  if(option == 1):
    enter_year = input('Enter in a year to sum up:  ')
    # print(enter_year)
    sum_annual_tlw(fishing_test, enter_year)

  if(option == 3):
    lower_limit = input('Enter in the lower limit year to analyze:  ')
    print(lower_limit)
    upper_limit = input('Enter in the upper limit year to analyze:  ')
    print(upper_limit)
    depletion_breakdown(fishing, fishing_test, lower_limit, upper_limit)

  if(option == 0):
    exit()


main_function()

#   #contains all of the functions and runs conditionally based on your decision
#menu on the gui/terminal to select functions you want to run
# do analysis on the years 
# add 2 more functions
# add a menu to choose a function
# modularize
# add matplotlib 