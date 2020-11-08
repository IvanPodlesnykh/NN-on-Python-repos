from datetime import datetime
import numpy as np
import pandas as pd
import MetaTrader5 as mt5
import pytz
import matplotlib.pyplot as plt
import mplfinance as mpf





""" Set timezone """

timezone = pytz.timezone("Etc/UTC")





""" Connect to MetaTrader 5 """

if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()





""" Get rates range """

eurusd_rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_D1, datetime(2020, 9, 1, tzinfo = timezone), datetime(2020, 10, 31, tzinfo = timezone))

#print(eurusd_rates)

print('_______________________________________________________________________________')

""" Shut down connection to MetaTrader 5 """

mt5.shutdown()





""" Pandas dataframe """

rates_frame = pd.DataFrame(eurusd_rates)

rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s')

print(rates_frame)

print('_______________________________________________________________________________')

ohlc = rates_frame[['open', 'high', 'low', 'close']]





""" Plot building """

# ohlc.index = rates_frame['time']

# mpf.plot(ohlc, type='candle', show_nontrading=True)





"""Adding body, upper shadow and lower shadow """

temp = ohlc.to_numpy()

types = []
body = []
upper_shadow = []
lower_shadow = []
for op, hi, lo, cl in temp:
    if cl > op:
        types.append('bull')
        body.append(cl - op)
        upper_shadow.append(hi - cl)
        lower_shadow.append(op - lo)
    elif cl < op:
        types.append('bear')
        body.append(op - cl)
        upper_shadow.append(hi - op)
        lower_shadow.append(cl - lo)
    else:
        types.append('doji')
        body.append(0)
        upper_shadow.append(hi - cl)
        lower_shadow.append(op - lo)

ohlc.insert(len(ohlc.columns), 'type', types)
ohlc.insert(len(ohlc.columns), 'body', body)
ohlc.insert(len(ohlc.columns), 'upper shadow', upper_shadow)
ohlc.insert(len(ohlc.columns), 'lower shadow', lower_shadow)





""" _________________________ Patterns analysis_____________________ """
temp = ohlc.to_numpy()
medium_body = 0
for i in range(len(temp) - 1):
    medium_body += temp[i][5]
medium_body = medium_body / len(temp)





""" ______________________Downtrend patterns analysis_____________________ """

temp = ohlc.to_numpy()

""" Bearish marubozu """
found = 0
successful = 0

for i in range(len(temp) - 2):
    if temp[i][4] == 'bear' and temp[i][5] != 0 and temp[i][6] == 0 and temp[i][7] == 0:
        found += 1
        if temp[i + 1][4] == 'bear':
            successful += 1

if found:
    print("Bearish marubozu: found = " + str(found) + ", successful = " + str(successful))
    print("Bearish marubozu success rate = " + str(successful / found * 100) + "%")

else: print("Bearish marubozu not found")
print("\n")


""" Bearish engulfing """
found = 0
successful = 0

for i in range(len(temp) - 3):
    if temp[i][4] == 'bull' and temp[i + 1][4] == 'bear' and temp[i][3] < temp[i + 1][0] \
        and temp[i][0] > temp[i + 1][3] and temp[i][6] < temp[i][5] \
        and temp[i][7] < temp[i][5] and temp[i + 1][6] \
        < temp[i + 1][5] and temp[i + 1][7] < temp[i + 1][5]:
        found += 1
        if temp[i + 2][4] == 'bear':
            successful +=1

if found:
    print("Bearish engulfing: found = " + str(found) + ", successful = " + str(successful))
    print("Bearish engulfing success rate = " + str(successful / found * 100) + "%")

else: print("Bearish engulfing not found")
print("\n")


""" Bearish harami """
found = 0
successful = 0

for i in range(len(temp) - 3):
    if temp[i][4] == 'bull' and temp[i + 1][4] == 'bear' and temp[i][3] > temp[i + 1][0] \
        and temp[i][0] < temp[i + 1][3] and temp[i][6] < temp[i][5] \
        and temp[i][7] < temp[i][5] and temp[i + 1][6] \
        < temp[i + 1][5] and temp[i + 1][7] < temp[i + 1][5]:
        found += 1
        if temp[i + 2][4] == 'bear':
            successful +=1

if found:
    print("Bearish harami: found = " + str(found) + ", successful = " + str(successful))
    print("Bearish harami success rate = " + str(successful / found * 100) + "%")

else: print("Bearish harami not found")
print("\n")


""" Three black crows """
found = 0
successful = 0

for i in range(len(temp) - 4):
    if temp[i][4] == 'bear' and temp[i + 1][4] == 'bear' and temp[i + 2][4] == 'bear' and \
       abs(temp[i][5] - medium_body) / medium_body * 100 <= 10 and \
       abs(temp[i + 1][5] - medium_body) / medium_body * 100 <= 10 and \
       abs(temp[i + 2][5] - medium_body) / medium_body * 100 <= 10 and \
       temp[i][6] < temp[i][5] and temp[i][7] < temp[i][5] and \
       temp[i + 1][6] < temp[i + 1][5] and temp[i + 1][7] < temp[i + 1][5] and \
       temp[i + 2][6] < temp[i + 2][5] and temp[i + 2][7] < temp[i + 2][5]:
           found += 1
           if temp[i + 3][4] == 'bear':
               successful += 1

if found:
    print("Three black crows: found = " + str(found) + ", successful = " + str(successful))
    print("Three black crows success rate = " + str(successful / found * 100) + "%")

else: print("Three black crows not found")
print("\n")


""" Evening star """
found = 0
successful = 0

for i in range(len(temp) - 4):
    if temp[i][4] == 'bull' and temp[i + 2][4] == 'bear' and temp[i + 1][5] <= temp[i][5] / 2 \
       and temp[i + 1][5] <= temp[i + 2][5] / 2:
           found += 1
           if temp[i + 3][4] == 'bear':
               successful += 1
    
if found:
    print("Evening star: found = " + str(found) + ", successful = " + str(successful))
    print("Evening star success rate = " + str(successful / found * 100) + "%")

else: print("Evening star not found")
print("\n")





""" _____________________Uptrend patterns analysis________________________ """

""" Bullish marubozu """
found = 0
successful = 0

for i in range(len(temp) - 2):
    if temp[i][4] == 'bull' and temp[i][5] != 0 and temp[i][6] == 0 and temp[i][7] == 0:
        found += 1
        if temp[i + 1][4] == 'bull':
            successful += 1

if found:
    print("Bullish marubozu: found = " + str(found) + ", successful = " + str(successful))
    print("Bullish marubozu success rate = " + str(successful / found * 100) + "%")

else: print("Bullish marubozu not found")
print("\n")


""" Bullish engulfing """
found = 0
successful = 0

for i in range(len(temp) - 3):
    if temp[i][4] == 'bear' and temp[i + 1][4] == 'bull' and temp[i][0] < temp[i + 1][3] \
        and temp[i][3] > temp[i + 1][0] and temp[i][6] < temp[i][5] \
        and temp[i][7] < temp[i][5] and temp[i + 1][6] \
        < temp[i + 1][5] and temp[i + 1][7] < temp[i + 1][5]:
        found += 1
        if temp[i + 2][4] == 'bull':
            successful +=1

if found:
    print("Bullish engulfing: found = " + str(found) + ", successful = " + str(successful))
    print("bullish engulfing success rate = " + str(successful / found * 100) + "%")

else: print("Bullish engulfing not found")
print("\n")


""" Bullish harami """
found = 0
successful = 0

for i in range(len(temp) - 3):
    if temp[i][4] == 'bear' and temp[i + 1][4] == 'bull' and temp[i][0] > temp[i + 1][3] \
        and temp[i][3] < temp[i + 1][0] and temp[i][6] < temp[i][5] \
        and temp[i][7] < temp[i][5] and temp[i + 1][6] \
        < temp[i + 1][5] and temp[i + 1][7] < temp[i + 1][5]:
        found += 1
        if temp[i + 2][4] == 'bull':
            successful +=1

if found:
    print("Bullish harami: found = " + str(found) + ", successful = " + str(successful))
    print("bullish harami success rate = " + str(successful / found * 100) + "%")

else: print("Bullish harami not found")
print("\n")


""" Three white soldiers """
found = 0
successful = 0

for i in range(len(temp) - 4):
    if temp[i][4] == 'bull' and temp[i + 1][4] == 'bull' and temp[i + 2][4] == 'bull' and \
       abs(temp[i][5] - medium_body) / medium_body * 100 <= 10 and \
       abs(temp[i + 1][5] - medium_body) / medium_body * 100 <= 10 and \
       abs(temp[i + 2][5] - medium_body) / medium_body * 100 <= 10 and \
       temp[i][6] < temp[i][5] and temp[i][7] < temp[i][5] and \
       temp[i + 1][6] < temp[i + 1][5] and temp[i + 1][7] < temp[i + 1][5] and \
       temp[i + 2][6] < temp[i + 2][5] and temp[i + 2][7] < temp[i + 2][5]:
           found += 1
           if temp[i + 3][4] == 'bull':
               successful += 1

if found:
    print("Three white soldiers: found = " + str(found) + ", successful = " + str(successful))
    print("Three white soldiers success rate = " + str(successful / found * 100) + "%")

else: print("Three white soldiers not found")
print("\n")


""" Morning star """
found = 0
successful = 0

for i in range(len(temp) - 4):
    if temp[i][4] == 'bear' and temp[i + 2][4] == 'bull' and temp[i + 1][5] <= temp[i][5] / 2 \
       and temp[i + 1][5] <= temp[i + 2][5] / 2:
           found += 1
           if temp[i + 3][4] == 'bull':
               successful += 1
    
if found:
    print("Morning star: found = " + str(found) + ", successful = " + str(successful))
    print("Morning star success rate = " + str(successful / found * 100) + "%")

else: print("Morning star not found")
print("\n")





""" Delete """
del(types, body, upper_shadow, lower_shadow, temp, op, hi, lo, cl, timezone, eurusd_rates, found, successful, i, medium_body)