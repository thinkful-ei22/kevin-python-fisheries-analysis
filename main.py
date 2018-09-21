import pandas as pd
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
      print(column)
      print(lower == column, lower)
      if lower == column:
        l_count+=1
      else:
        continue
      if l_count == 0: 
        raise KeyError('This is not a valid lower limit Year')
        break
      if upper == column:
        u_count+=1
      else:
        continue
      if u_count == 0:
        raise KeyError('This is not a valid upper limit Year')
        break
  except Exception as error: 
    print('Caught this error: ' + repr(error))

  for index, row in fishing.iterrows():
    # print(row, index)
    if row[upper] < row[lower]*.799:
      #.79 value retrieved from Technical Guidance On the Use of Precautionary
      #  Approaches to Implementing National Standard 1 of the
      # Magnuson-Stevens Fishery Conservation and Management Act 1998
      fishing.at[index, 'Depleted'] = 'Yes'
  # print(fishing)
  fishing_new_1 = fishing.loc[:, upper:lower]
  fishing_new_2 = fishing.loc[:, ['Depleted', 'Area', 'Species', 'Country']]
  fishing_new_new = pd.concat([fishing_new_1, fishing_new_2], axis=1)
  print(tabulate(fishing_new_new, headers='keys', tablefmt='grid'))
  
  original_data = len(original)
  print('There are %d total entries in the 2006-2016 ICES Nominal Catch Dataset.' % original_data, end='\n\n')
  filtered_data = len(fishing_data)
  print('Out of the %d, %d filtered entries are being analyzed that contain non-zero values.' % (original_data, len(fishing_test)), end='\n\n')
  df = fishing['Species'].value_counts()
  unique_species = len(df)
  print('There are %d unique species being caught in the Atlantic Northeast based on the year range.' % unique_species, end='\n\n')
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
  print('----------------------------------------------------------------------------', end='\n\n')
  main_function()
  #this discrepancy from 50,000+ to 7000 is likely due to some species of fish and shellfish being naturally rare/scarce in some waters

def sum_annual_tlw (fishing, year):
  try:
    count = 0
    for column in fishing:
      # print(column)
      # print(lower == column, lower)
      if year == column:
        count+=1
      else:
        continue
      if count == 0: 
        raise KeyError('This is not a valid lower limit Year')
        return
  except Exception as error: 
    print('Caught this error: ' + repr(error))

  tlw_annual = fishing[year].sum()
  year = int(year)
  print('----------------------------------------------------------------------------', end='\n\n')
  print('In %d, there was a total of %.2f TLW (tons live weight) fish and shellfish caught in the Northeast Atlantic.' % (year, tlw_annual), end='\n\n')
  print('----------------------------------------------------------------------------', end='\n\n')
  main_function()

def sum_aggregate_tlw_range (fishing, lower, upper):
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

  range_tlw = fishing.loc[:, upper:lower].sum(axis=1).sum()
  lower = int(lower)
  upper = int(upper)
  print('----------------------------------------------------------------------------', end='\n\n')
  print('From %d to %d, a total of %.2f TLW was caught.' % (lower, upper, range_tlw), end='\n\n')
  main_function()

def detailed_species_depletion (fishing, species):
  # print(species)
  # print(type (species))
  print(fishing)
  filtered_species_1 = fishing.loc[fishing['Species'] == species, '2016': '2006']
  # filtered_species_1.insert(len(filtered_species_1.columns), 'Depleted', 'No')
  # print(filtered_species_1)
  filtered_species_2 = fishing.loc[:, ['Depleted', 'Area', 'Country', 'Species']]
  # print(filtered_species_2)
  filtered_species_new = pd.concat([filtered_species_1, filtered_species_2], axis=1)
  filtered_species_new = filtered_species_new.dropna(axis='rows')
  
  print('---- Before Analysis ----')
  print(tabulate(filtered_species_new, headers='keys', tablefmt='grid'), end='\n\n')

  for index, row in filtered_species_new.iterrows():
    # print(row, index)
    if row['2016'] < row['2006']*.799:
      #.79 value retrieved from Technical Guidance On the Use of Precautionary
      #  Approaches to Implementing National Standard 1 of the
      # Magnuson-Stevens Fishery Conservation and Management Act 1998
      filtered_species_new.at[index, 'Depleted'] = 'Yes'

  print('---- After Analysis ----')
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
  print('----------------------------------------------------------------------------', end='\n\n')
  main_function()

def area_code_breakdown (fishing, area_code, filter_by_year):
  print(fishing)
  # print(area_code)
  # print(type (area_code))
  if filter_by_year != 'none':
    filtered_area_1 = fishing.loc[fishing['Area'] == area_code, filter_by_year]
  elif filter_by_year == 'none':
    filtered_area_1 = fishing.loc[fishing['Area'] == area_code, '2016': '2006']

  # filtered_species_1.insert(len(filtered_species_1.columns), 'Depleted', 'No')
  # print(filtered_species_1)
  filtered_area_2 = fishing.loc[:, ['Depleted', 'Country', 'Species', 'Area']]
  # print(filtered_species_2)
  filtered_area_new = pd.concat([filtered_area_1, filtered_area_2], axis=1)
  filtered_area_new = filtered_area_new.dropna(axis='rows')
  # filtered_area.insert(len(filtered_area.columns), 'Depleted', 'No')
  print('---- Before Analysis ----')
  print(tabulate(filtered_area_new, headers='keys', tablefmt='grid'), end='\n\n')
  for index, row in filtered_area_new.iterrows():
    # print(row, index)
    if row['2016'] < row['2006']*.799:
      #.79 value retrieved from Technical Guidance On the Use of Precautionary
      #  Approaches to Implementing National Standard 1 of the
      # Magnuson-Stevens Fishery Conservation and Management Act 1998
      filtered_area_new.at[index, 'Depleted'] = 'Yes'

  print('---- After Analysis ----')
  print(tabulate(filtered_area_new, headers='keys', tablefmt='grid'), end='\n\n')
  depletion_totals = filtered_area_new['Depleted'].value_counts()
  print(depletion_totals)
  # print(depletion_totals['No'])
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
  print('----------------------------------------------------------------------------', end='\n\n')
  main_function()

def main_function ():
  print('Available Functions:', end='\n\n')
  print('Numerical Analysis:', end='\n\n')
  print('Enter 1 to Determine Total Annual Catch for a Year.')
  print('Enter 2 to Determine Aggregate Catch for a Range of Years.')
  print('Enter 3 to do Quantitative Analysis of the Health of Fishery Stocks.')
  print('Enter 4 to do Quantitative Analysis of the Health of a Specific Fish Species.')
  print('Enter 5 to do Quantitative Analysis of the Health in a specific Area Code', end='\n\n')
  print('Graphical Representation:', end='\n\n')
  print('Bar Graph of each Years Annual TLW from 2006 to 2016.')
  print('Pie Chart of each Species and its Depletion Percentage.', end='\n\n')
  
  option = input('Enter in an option to run an analytical function (or 0 to exit):  ')
  option = int(option)
  # print(option)
  if option == 1:
    enter_year = input('Enter in a year to sum up:  ')
    # print(enter_year)
    sum_annual_tlw(fishing_test, enter_year)

  if option == 2:
    lower_limit = input('Enter in the lower limit year to aggregate:  ')
    print(lower_limit)
    upper_limit = input('Enter in the upper limit year to aggregate (inclusive):  ')
    print(upper_limit)
    sum_aggregate_tlw_range(fishing_test, lower_limit, upper_limit)

  if option == 3:
    lower_limit = input('Enter in the lower limit year to analyze:  ')
    print(lower_limit)
    upper_limit = input('Enter in the upper limit year to analyze:  ')
    print(upper_limit)
    depletion_breakdown(fishing, fishing_test, lower_limit, upper_limit)

  if option == 4:
    species_abbrev = input('Enter in a species abbreviation to analyze:  ')
    print(species_abbrev)
    detailed_species_depletion(fishing_test, species_abbrev)
  
  if option == 5:
    area_code = input('Enter in an area code to analyze:  ')
    print(area_code)
    filter_by_year_question = input('Do you want to filter by Year as well? -- Yes or No  ')
    if(filter_by_year_question == 'Yes'):
      filter_by_year = input('Enter the year you would like to filter by:  ')
      area_code_breakdown(fishing_test, area_code, filter_by_year)
    elif(filter_by_year_question == 'No'):
      area_code_breakdown(fishing_test, area_code, 'none')

  if option == 0:
    exit()


main_function()

#   #contains all of the functions and runs conditionally based on your decision
#menu on the gui/terminal to select functions you want to run
# modularize
# add matplotlib 