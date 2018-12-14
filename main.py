import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt 
from tabulate import tabulate
from NumSpecies import log_number_of_species
from AnnualSum import sum_annual_tlw
from SumRange import sum_aggregate_tlw_range
from DetailedDepletion import detailed_species_depletion
from AreaCode import area_code_breakdown
from BarGraph import bar_graph_per_annum_tlw
fishing = pd.read_csv('ICESCatchDataset2006-2016.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

fishing = fishing[['Species', 'Area', 'Country', 
'2016', '2015', '2014', '2013', '2012', '2011', 
'2010', '2009', '2008', '2007', '2006' ]]

fishing_data = fishing.dropna(axis='rows')
fishing_data = fishing_data[(fishing_data != 0).all(1)]
################ Here, you can size down the Pandas Data Frame to analyze smaller subsets of the data ##################
# fishing_test = fishing_data[8:14]
fishing_test = fishing_data
#It is currently set to analyzing the full subset of non-zero values -- all 7343 entries of the 52,517 that are non-zero
########################################################################################################################
fishing_test.insert(len(fishing_test.columns), 'Depleted', 'No')
# values each year are in the units of TLW -- tons of live weight
# species are denoted by an abbreviation ex. ANF

def depletion_breakdown (original, fishing, lower, upper): 
  try:
    l_count = 0
    u_count = 0

    for column in fishing:
      # print(column)
      # print(l_count)
      if lower == column:
        l_count+=1
      elif upper == column:
        u_count+=1
      else:
        continue

    if l_count == 0: 
      raise KeyError('This is not a valid lower limit Year.')
      return
    if u_count == 0:
      raise KeyError('This is not a valid upper limit Year.')
      return

  except Exception as error: 
    print('Caught this error: ' + repr(error))
    return
    
  for index, row in fishing.iterrows():
    # print(row, index)
    if row[upper] < row[lower]*.799:
      #.799 value retrieved from Technical Guidance On the Use of Precautionary
      # Approaches to Implementing National Standard 1 of the
      # Magnuson-Stevens Fishery Conservation and Management Act 1998
      fishing.at[index, 'Depleted'] = 'Yes'

  fishing_new_1 = fishing.loc[:, upper:lower]

  fishing_new_2 = fishing.loc[:, ['Depleted', 'Area', 'Species', 'Country']]

  fishing_new_new = pd.concat([fishing_new_1, fishing_new_2], axis=1)

  #Output
  print('----------------------------------------------------------------------------')
  print('Analysis:', end='\n\n')
  print(tabulate(fishing_new_new, headers='keys', tablefmt='grid'))
  original_data = len(original)
  print('There are %d total entries in the 2006-2016 ICES Nominal Catch Dataset.' % original_data, end='\n\n')
  filtered_data = len(fishing_data)
  print('Out of the %d, %d filtered entries are being analyzed that contain non-zero values.' % (original_data, len(fishing_test)), end='\n\n')
  df = fishing['Species'].value_counts()
  unique_species = len(df)
  lower = int(lower)
  upper = int(upper)
  print('You have filtered these entries to years: %d - %d from the original 2006 - 2016.' %(lower, upper))
  print('This may or may not alter the depleted status of the entries.', end='\n\n')
  print('There are %d unique fish and shellfish species being caught during this year range' % unique_species)
  print('by participating European Countries in the Atlantic Northeast.', end='\n\n')
  
  depletion_totals = fishing_test['Depleted'].value_counts()
  
  if depletion_totals.index.str.contains('Yes').any():
    depl_yes = int(depletion_totals['Yes'])
  else:
    depl_yes = 0

  if depletion_totals.index.str.contains('No').any():
    depl_no = int(depletion_totals['No'])
  else:
    depl_no = 0

  percentage = (depl_yes/(depl_no+depl_yes))*100

  print('There are %d entries that are classified as depleted and %d entries that are not -- a percentage'  % (depl_yes, depl_no))
  print('of %.2f%% based on a TAC value of 0.80 - Total Allowable Catch - to maintain sustainability.' % percentage)
  print('----------------------------------------------------------------------------')
  #this discrepancy from 50,000+ to 7000 is likely due to some species of fish and shellfish being naturally rare/scarce in some waters
  main_function()

def analyzing_in_progress ():
  print('Analyzing...', end='\n\n')
  print('3... 2... 1...', end='\n\n')


def main_function ():
  #Menu
  print('|==========================================================================|')
  print('Available Functions:', end='\n\n')
  print('Numerical Analysis:', end='\n\n')
  print('Enter 1 to Analyze the Number of Species being recorded.')
  print('Enter 2 to Determine Total Annual Catch for a Year.')
  print('Enter 3 to Determine Aggregate Catch for a Range of Years.')
  print('Enter 4 to do Quantitative Analysis of the Health of Fishery Stocks.')
  print('Enter 5 to do Quantitative Analysis of the Health of a Specific Fish Species.')
  print('Enter 6 to do Quantitative Analysis of the Health in a specific Area Code.', end='\n\n')
  print('Graphical Representation:', end='\n\n')
  print('Enter 7 to Display a Bar Graph of each Years Annual TLW from 2006 to 2016.')
  print('Enter 8 to Display a Pie Chart of each Species and its Depletion Percentage.', end='\n\n')
  print('|==========================================================================|')
  
  option = input('Enter in an option to run an analytical function (or 0 to exit):  ')
  option = int(option)
  if option == 1:
    analyzing_in_progress()
    log_number_of_species(fishing)
    main_function()

  if option == 2:
    enter_year = input('Enter in a year to sum up:  ')
    print(enter_year)
    analyzing_in_progress()
    sum_annual_tlw(fishing_test, enter_year)
    main_function()

  if option == 3:
    lower_limit = input('Enter in the lower limit year to aggregate:  ')
    print(lower_limit)
    upper_limit = input('Enter in the upper limit year to aggregate (inclusive):  ')
    print(upper_limit)
    analyzing_in_progress()
    sum_aggregate_tlw_range(fishing_test, lower_limit, upper_limit)
    main_function()

  if option == 4:
    lower_limit = input('Enter in the lower limit year to analyze:  ')
    print(lower_limit)
    upper_limit = input('Enter in the upper limit year to analyze:  ')
    print(upper_limit)
    analyzing_in_progress()
    depletion_breakdown(fishing, fishing_test, lower_limit, upper_limit)

  if option == 5:
    species_abbrev = input('Enter in a species abbreviation to analyze:  ')
    print(species_abbrev)
    analyzing_in_progress()
    detailed_species_depletion(fishing_test, species_abbrev)
    main_function()
  
  if option == 6:
    area_code = input('Enter in an area code to analyze:  ')
    # print(area_code)
    filter_by_year_question = input('Do you want to filter by Year as well? -- Yes or No  ')
    if(filter_by_year_question == 'Yes'):
      filter_by_year_lower = input('Enter the lower limit year you would like to filter by:  ')
      print(filter_by_year_lower)
      filter_by_year_upper = input('Enter the upper limit year you would like to filter by (inclusive):  ')
      print(filter_by_year_upper)
      analyzing_in_progress()
      area_code_breakdown(fishing_test, area_code, filter_by_year_lower, filter_by_year_upper)
      main_function()
    elif(filter_by_year_question == 'No'):
      analyzing_in_progress()
      area_code_breakdown(fishing_test, area_code, '2006', '2016')
      main_function()
  
  if option == 7:
    bar_graph_per_annum_tlw(fishing_test)
    main_function()
  
  if option == 8:
    print('Not yet Implemented')
    exit()

  if option == 0:
    print('Thank you for using this program!')
    exit()


main_function()

# modularize if time