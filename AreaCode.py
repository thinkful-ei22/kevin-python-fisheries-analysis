import pandas as pd
from tabulate import tabulate

def area_code_breakdown (fishing, area_code, lower, upper):
  try:
    area_count = 0
    l_count = 0
    u_count = 0

    if (fishing['Area'] == area_code).any():
      area_count+=1 

    for column in fishing:
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

  filtered_area_2 = fishing.loc[:, ['Depleted', 'Country', 'Species', 'Area']]

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