import pandas as pd
from tabulate import tabulate

fishing = pd.read_csv('ICESCatchDataset2006-2016.csv')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

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

  filtered_species_2 = fishing.loc[:, ['Depleted', 'Area', 'Country', 'Species']]
 
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