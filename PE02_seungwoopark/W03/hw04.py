#2021073863 박승우
import matplotlib.pyplot as plt    #set as plt to use matplotlib
import numpy as np                 #set as np to ise numpy
x = np.linspace(-10, 10, 100)   #set the x-axis range
y = x ** 3  #set y-axis value that is contrast with x value
plt.plot(x, y)  #to plot gtaph, set the x-coordinate, y-coordinate.
plt.xscale('symlog')    #set y-axis scale to log
plt.show()  #plot the graph on the screen