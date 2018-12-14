import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def bar_graph_per_annum_tlw (fishing):
  years = fishing.columns[3:14]
  sum_each_year = fishing[:].sum().values[3:14]
  # print(sum_each_year)
  sum_new = []

  for x,y in enumerate(sum_each_year):
    y = math.floor(y)
    sum_new.append(y)

  # print(sum_new, sum_new[0], type(sum_new[0]))
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