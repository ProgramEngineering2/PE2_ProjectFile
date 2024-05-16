#2021073863 박승우
import numpy as np  #set as np to use numpy
import pandas as pd #set as pd to use pandas

cols = ['국어', '수학', '영어', '과학', '사회']   #set columns' name list as cols
lists = [[83, 68, 92, 55, 85], [40, 95, 64, 87, 77], [ 65, 87, 58, 92, 72]] #make 3 lists that will be used for values
indexes = ['태현', '준수', '기준']    #set indexs' name list as indexes
dfs = pd.DataFrame(lists, columns=cols, index=indexes)  #set lists for value, cols for columns, indexes for index
print(dfs)  #print it

dfs.to_csv("./hw10_result.csv")