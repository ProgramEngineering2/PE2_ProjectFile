#2021073863 박승우
import matplotlib.pyplot as plt     #set as plt to use matplotlib
import numpy as np  #set as np to ise numpy
x = np.arange(0, 2, 0.2)    #set the x-axis range and make dot at 0.2 intervals
plt.plot(x, x, 'r--', x, x**2, 'bo', x, x**3, 'g-.')    #set a coordinate and set a color and shape of graph
plt.show()      #plot the graph on the screen