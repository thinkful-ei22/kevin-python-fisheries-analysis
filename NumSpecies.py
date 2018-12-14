def log_number_of_species (fishing):
  species_log = len(fishing['Species'].value_counts())
  #Output
  print('----------------------------------------------------------------------------')
  print('Analysis:', end='\n\n')
  print('A total of %d unique fish and shellfish species were caught and recorded in the 2006-2016 ' % (species_log), end='\n\n')
  print('ICES Nominal Catch Dataset by participating European Countries in the Altantic Northeast.')
  print('----------------------------------------------------------------------------')
