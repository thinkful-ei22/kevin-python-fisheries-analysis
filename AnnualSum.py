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