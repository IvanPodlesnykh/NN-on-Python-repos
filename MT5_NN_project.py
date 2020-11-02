import MetaTrader5 as mt5
import numpy as np
from NN_class import NeuralNetwork

NN = NeuralNetwork([5, 5, 3, 1])

inpu = np.array([1, 2, 3, 4, 5]).reshape(5,1)

test = NN.feedforward(inpu)

print(test[0])



#mt5.initialize()
#mt5.shutdown()