import numpy as np
import random

##########################################################
"""Дополнительные функции"""
##########################################################

def Sigmoid(x):
    return 1 / (1 + np.exp(-x))

def Sigmoid_prime(x):
    """
    Производная сигмоиды
    """
    return Sigmoid(x) * (1 - Sigmoid(x))

def Cost_func(neural_network, data):
    """
    Квадратичная целевая функция
    """
    cost = 0
    for example, y in data:
        yhat = neural_network.feedforward(example)
        cost += np.sum((y - yhat)**2)
    return cost / len(data)

##########################################################
"""Класс нейронной сети"""
##########################################################

class NeuralNetwork:

    def __init__(self, sizes):
        """
        Список sizes содержит количество нейронов в соответствующих слоях
        нейронной сети 
        """

        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        """
        Выходная активация нейронной сети
        """
        for b, w in zip(self.biases, self.weights):
            a = Sigmoid(np.dot(w, a)+b)
        return a

    def SGD(self, training_data, epochs, mini_batch_size, eta,
            test_data=None):
        """
        Алгоритм стохастического mini-batch градиентного спуска. 
        training_data - лист кортежей вида (x, y), где 
        x - вход обучающего примера, y - желаемый выход
        """
        
        #if test_data is not None: n_test = len(test_data)
        n = len(training_data)
        #successful_tests = 0
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [
                training_data[k:k+mini_batch_size]
                for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, eta)
            #if test_data is not None:
                #successful_tests = self.evaluate(test_data)
                #print("Эпоха {0}: {1} / {2}".format(
                    #j, successful_tests, n_test))
            #else:
                #print("Эпоха {0} завершена".format(j))
        #if test_data is not None:
            #return successful_tests / n_test

    def update_mini_batch(self, mini_batch, eta):
        """
        Обновить веса и смещения нейронной сети, сделав шаг градиентного
        спуска на основе алгоритма обратного распространения ошибки, примененного
        к одному mini batch.
        mini_batch - список кортежей вида (x, y),
        eta - величина шага (learning rate).
        """
        
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb+dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw+dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            
        eps = eta / len(mini_batch)
        self.weights = [w - eps * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases  = [b - eps * nb for b, nb in zip(self.biases,  nabla_b)]

    def backprop(self, x, y):
        """
        Возвращает кортеж (nabla_b, nabla_w) - градиент целевой функции по всем параметрам сети.
        nabla_b и nabla_w - послойные списки массивов ndarray,
        такие же, как self.biases и self.weights соответственно.
        """
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        # прямое распространение (forward pass)
        activation = x
        activations = [x] # лист всех активаций слой за слоем
        zs = []
        
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation)+b
            zs.append(z)
            activation = Sigmoid(z)
            activations.append(activation)

        # обратное распространение (backward pass)
        delta = self.cost_derivative(activations[-1], y) * Sigmoid_prime(zs[-1]) # ошибка выходного слоя
        nabla_b[-1] =  delta # производная J по смещениям выходного слоя
        nabla_w[-1] =  np.dot(delta, activations[-2].transpose()) # производная J по весам выходного слоя

        # l = 1 последний слой, 
        # l = 2 - предпоследний слой
        
        for l in range(2, self.num_layers):
            z = zs[-l]
            delta = np.dot(self.weights[-l+1].transpose(), delta) * Sigmoid_prime(z) # ошибка на слое L-l
            nabla_b[-l] = delta # производная J по смещениям L-l-го слоя
            nabla_w[-l] = np.dot(delta, activations[-l-1].transpose()) # производная J по весам L-l-го слоя
        return nabla_b, nabla_w
    
    #def evaluate(self, test_data):
        #"""
        #Возвращает количество тестовых примеров, для которых нейронная сеть
        #возвращает правильный ответ.
        #"""
        #test_results = [(np.argmax(self.feedforward(x)), y)
                        #for (x, y) in test_data]
        #return sum(int(x == y) for (x, y) in test_results)
    
    def cost_derivative(self, output_activations, y):
        """
        Возвращает вектор частных производных (\partial C_x) / (\partial a) 
        целевой функции по активациям выходного слоя.
        """
        return (output_activations-y)
    
