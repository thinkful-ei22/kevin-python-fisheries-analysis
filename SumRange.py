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
  print('From %d to %d, a total of %.2f TLW fish and shellfish were reportedly caught in European Waters.' % (lower, upper, range_tlw), end='\n\n')
  print('----------------------------------------------------------------------------')