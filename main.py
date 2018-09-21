import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt 
from tabulate import tabulate

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

def log_number_of_species (fishing):
  species_log = len(fishing['Species'].value_counts())
  #Output
  print('----------------------------------------------------------------------------')
  print('Analysis:', end='\n\n')
  print('A total of %d unique fish and shellfish species were caught and recorded in the 2006-2016 ' % (species_log), end='\n\n')
  print('ICES Nominal Catch Dataset by participating European Countries in the Altantic Northeast.')
  print('----------------------------------------------------------------------------')
  main_function()


def sum_annual_tlw (fishing, year):
  try:
    count = 0

    for column in fishing:
      if year == column:
        count+=1
      else:
        continue

    if count == 0: 
      raise KeyError('This is not a valid Year.')
      return

  except Exception as error: 
    print('Caught this error: ' + repr(error))
    return

  tlw_annual = fishing[year].sum()
  year = int(year)
  #Output
  print('----------------------------------------------------------------------------')
  print('Analysis:', end='\n\n')
  print('In %d, there was a total of %.2f TLW (tons live weight) fish and shellfish caught in the Northeast Atlantic.' % (year, tlw_annual), end='\n\n')
  print('----------------------------------------------------------------------------')
  main_function()


def sum_aggregate_tlw_range (fishing, lower, upper):
  try:
    l_count = 0
    u_count = 0
    for column in fishing:
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

  range_tlw = fishing.loc[:, upper:lower].sum(axis=1).sum()
  lower = int(lower)
  upper = int(upper)
  #Output
  print('----------------------------------------------------------------------------')
  print('Analysis:', end='\n\n')
  print('From %d to %d, a total of %.2f TLW fish and shellfish were caught.' % (lower, upper, range_tlw), end='\n\n')
  print('----------------------------------------------------------------------------')
  main_function() 


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
  main_function()
  #this discrepancy from 50,000+ to 7000 is likely due to some species of fish and shellfish being naturally rare/scarce in some waters

def detailed_species_depletion (fishing, species):
  try:
    count = 0
    if (fishing['Species'] == species).any():
      count+=1

    if count == 0: 
      raise KeyError('This is not a valid Species Abbreviation. Examples: ANF, GUU')
      return

  except Exception as error: 
    print('Caught this error: ' + repr(error))
    return

  filtered_species_1 = fishing.loc[fishing['Species'] == species, '2016': '2006']
  # print(filtered_species_1)
  filtered_species_2 = fishing.loc[:, ['Depleted', 'Area', 'Country', 'Species']]
  # print(filtered_species_2)
  filtered_species_new = pd.concat([filtered_species_1, filtered_species_2], axis=1)
  filtered_species_new = filtered_species_new.dropna(axis='rows')
  
  # print(tabulate(filtered_species_new, headers='keys', tablefmt='grid'), end='\n\n')

  for index, row in filtered_species_new.iterrows():
    # print(row, index)
    if row['2016'] < row['2006']*.799:
      #.799 value retrieved from Technical Guidance On the Use of Precautionary
      # Approaches to Implementing National Standard 1 of the
      # Magnuson-Stevens Fishery Conservation and Management Act 1998
      filtered_species_new.at[index, 'Depleted'] = 'Yes'

  #Output
  print('----------------------------------------------------------------------------')
  print('Analysis:', end='\n\n')
  print(tabulate(filtered_species_new, headers='keys', tablefmt='grid'), end='\n\n')

  depletion_totals = filtered_species_new['Depleted'].value_counts()

  if depletion_totals.index.str.contains('Yes').any():
    depl_yes = int(depletion_totals['Yes'])
  else:
    depl_yes = 0

  if depletion_totals.index.str.contains('No').any():
    depl_no = int(depletion_totals['No'])
  else:
    depl_no = 0

  proportion = depl_yes/(depl_no+depl_yes)
  percentage = proportion*100

  print('Based on data analysis, this species -- %s -- shows depleted status on %.2f%% of the areas it is fished in \n the past decade, from 2006 to 2016.'  % (species, percentage))
  print('This is based on a TAC value of 0.80 - Total Allowable Catch - to maintain sustainability.', end='\n\n')
  print('----------------------------------------------------------------------------')
  main_function()


def area_code_breakdown (fishing, area_code, lower, upper):
  try:
    area_count = 0
    l_count = 0
    u_count = 0

    if (fishing['Area'] == area_code).any():
      area_count+=1 

    for column in fishing:
      # print(column)
      if lower == column:
        l_count+=1
      elif upper == column:
        u_count+=1
      else:
        continue

    if area_count == 0: 
      raise KeyError('This is not a valid Area Code.')
      return
    if l_count == 0: 
      raise KeyError('This is not a valid lower limit Year.')
      return
    if u_count == 0:
      raise KeyError('This is not a valid upper limit Year.')
      return

  except Exception as error: 
    print('Caught this error: ' + repr(error))
    return

  filtered_area_1 = fishing.loc[fishing['Area'] == area_code, upper:lower]

  # print(filtered_area_1)
  filtered_area_2 = fishing.loc[:, ['Depleted', 'Country', 'Species', 'Area']]
  # print(filtered_area_2)
  filtered_area_new = pd.concat([filtered_area_1, filtered_area_2], axis=1)

  filtered_area_new = filtered_area_new.dropna(axis='rows')
  # print(tabulate(filtered_area_new, headers='keys', tablefmt='grid'), end='\n\n')
  for index, row in filtered_area_new.iterrows():
    # print(row, index)
    if row[upper] < row[lower]*.799:
      #.799 value retrieved from Technical Guidance On the Use of Precautionary
      # Approaches to Implementing National Standard 1 of the
      # Magnuson-Stevens Fishery Conservation and Management Act 1998
      filtered_area_new.at[index, 'Depleted'] = 'Yes'

  #Output
  print('----------------------------------------------------------------------------')
  print('Analysis:', end='\n\n')
  print(tabulate(filtered_area_new, headers='keys', tablefmt='grid'), end='\n\n')

  depletion_totals = filtered_area_new['Depleted'].value_counts()
  # print(depletion_totals)

  if depletion_totals.index.str.contains('Yes').any():
    depl_yes = int(depletion_totals['Yes'])
  else:
    depl_yes = 0

  if depletion_totals.index.str.contains('No').any():
    depl_no = int(depletion_totals['No'])
  else:
    depl_no = 0

  percentage = (depl_yes/(depl_no+depl_yes))*100

  print('Based on data analysis, this area code -- %s -- shows depleted status on %.2f%% of the entries it is fished in \n the past decade, from 2006 to 2016.'  % (area_code, percentage))
  print('This is based on a TAC value of 0.80 - Total Allowable Catch - to maintain sustainability.', end='\n\n')
  print('----------------------------------------------------------------------------')
  main_function()


def bar_graph_per_annum_tlw (fishing):
  years = fishing.columns[3:14]
  sum_each_year = fishing[:].sum().values[3:14]
  # print(sum_each_year)
  sum_new = []

  for x,y in enumerate(sum_each_year):
    # print(y)
    y = math.floor(y)
    sum_new.append(y)

  print(sum_new, sum_new[0], type(sum_new[0]))
  # year_annum = sum_everything.loc[3:14]
  y_pos = np.arange(len(years))
  # print(sum_new, max(sum_new), min(sum_new))
  plt.bar(y_pos, sum_new)

  plt.ylim([min(sum_new) - (min(sum_new)*.03), max(sum_new) + (max(sum_new)*.03)])

  plt.xticks(y_pos, years)

  plt.ylabel('Tons of Live Weight (x10⁷)')

  plt.xlabel('Year')

  plt.title('Aggregated Catch Data per Annum in Northeast Atlantic (2006-2016)')

  for a,b in enumerate(sum_new):
    plt.text(a, b, str(b), fontsize=9, horizontalalignment='center')
  plt.show()
  # plt.savefig("BarGraphOf6.png") 
  # saves the graph into the project folder
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

  if option == 2:
    enter_year = input('Enter in a year to sum up:  ')
    print(enter_year)
    analyzing_in_progress()
    sum_annual_tlw(fishing_test, enter_year)

  if option == 3:
    lower_limit = input('Enter in the lower limit year to aggregate:  ')
    print(lower_limit)
    upper_limit = input('Enter in the upper limit year to aggregate (inclusive):  ')
    print(upper_limit)
    analyzing_in_progress()
    sum_aggregate_tlw_range(fishing_test, lower_limit, upper_limit)

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
  
  if option == 6:
    area_code = input('Enter in an area code to analyze:  ')
    print(area_code)
    filter_by_year_question = input('Do you want to filter by Year as well? -- Yes or No  ')
    if(filter_by_year_question == 'Yes'):
      filter_by_year_lower = input('Enter the lower limit year you would like to filter by:  ')
      print(filter_by_year_lower)
      filter_by_year_upper = input('Enter the upper limit year you would like to filter by (inclusive):  ')
      print(filter_by_year_upper)
      analyzing_in_progress()
      area_code_breakdown(fishing_test, area_code, filter_by_year_lower, filter_by_year_upper)
    elif(filter_by_year_question == 'No'):
      analyzing_in_progress()
      area_code_breakdown(fishing_test, area_code, '2006', '2016')
  
  if option == 7:
    bar_graph_per_annum_tlw(fishing_test)
  
  if option == 8:
    print('Not yet Implemented')
    exit()

  if option == 0:
    print('Thank you for using this program!')
    exit()


main_function()

# modularize if time