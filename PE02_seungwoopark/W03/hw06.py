#2021073863 박승우
import numpy as np  #set as np to use numpy
import pandas as pd #set as pd to use pandas

cols = ['col1', 'col2', 'col3'] #set a column name
list2 = [[1, 2, 3], [11, 12, 13]]   #make a list with values that will be included in the table
df_list2 = pd.DataFrame(list2, columns=cols)    #set a table as df_list2. list2 will be used for the values and cols will be used for column
print(df_list2)     #print the table