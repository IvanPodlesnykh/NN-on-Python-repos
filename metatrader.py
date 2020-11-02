from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
 
# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
 
# request connection status and parameters
print(mt5.terminal_info())
# get data on MetaTrader 5 version
print(mt5.version())
 
# request ticks from EURRUB within range
eurrub_ticks = mt5.copy_ticks_range("EURRUB", datetime(2020,10,27,13), datetime(2020,10,28,13), mt5.COPY_TICKS_ALL)
 
# shut down connection to MetaTrader 5
mt5.shutdown()
 
#DATA
print('eurrub_ticks(', len(eurrub_ticks), ')')
for val in eurrub_ticks[:10]: print(val)
 

#PLOT
# create DataFrame out of the obtained data
ticks_frame = pd.DataFrame(eurrub_ticks)
# convert time in seconds into the datetime format
ticks_frame['time']=pd.to_datetime(ticks_frame['time'], unit='s')
# display ticks on the chart
plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')
 
# display the legends
plt.legend(loc='upper left')
 
# add the header
plt.title('EURRUB ticks')
 
# display the chart
plt.show()