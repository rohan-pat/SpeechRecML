import numpy as np
import random
from math import exp
import decimal

class HiddenNeuron:
    """ Class for hidden neurons. 10 neurons.
        Each with 13 inputs and a bias.
        Starting with random weights and bias.
    """
    def __init__(self, i):
        # two weights for 2 inputs and 1 bias into 13 counting for each input.
        weight = random.sample(range(1,100), 14)
        # power = random.sample(range(1,5),1)
        self.weight_vector = np.array(weight, dtype=float) # wji.
        self.weight_vector = (self.weight_vector / 100) #* ((-1) ** power[0])
        self.output = decimal.Decimal(0.0) # hj
        self.id = "H" + str(i+1) # for printing purposes.

class OutputNeuron:
    """ Class structure for output neuron.
        Each with 10 input from hidden neurons and a bias.
        Starting with random weights and bias.
    """
    def __init__(self, i):
        weight = random.sample(range(1,100), 11)
        self.weight_vector = np.array(weight, dtype=float) # wj
        self.weight_vector = self.weight_vector / 1000
        self.output = 0.0 # o
        self.id = "O" + str(i+1)

def activation_function(x):
    # exponential function as activation
    # using decimal to better handle floating point underflow.
    x = decimal.Decimal(-x)
    z = x.exp()
    return float(round(decimal.Decimal(1) / decimal.Decimal(1 + z), 8))
    # # sign function as activation
    # if x >= 0.0:
    #     return 1
    # else:
    #     return 0

def forward_pass(feature, hidden_neuron, output_neuron):
    """ Calculating the hidden output during the forward pass.
        and then calculating the output of the output node.
    """
    # calculating hjs using the input weights
    hj_list = []
    # appended with 1 to deal with the bias for the output node.
    hj_list.append(1)
    for h in hidden_neuron:
        h.output = activation_function(np.sum(feature * h.weight_vector))
        hj_list.append(h.output)

    hj_array = np.array(hj_list, dtype=float)
    # print(hj_array)

    # calculate output using the hj * wj.
    output_neuron.output = activation_function(np.sum(hj_array * output_neuron.weight_vector))
    return hj_array

def back_propogation(feature, hidden_neuron, output_neuron, hj_array, target):
    """ changing weights of the output node first and then using the changed weights for
        calculating weights of hidden nodes.
    """
    learning_rate = 0.43
    # sigmoidal output for output node.
    op = output_neuron.output
    # calculating the weights of output node.
    n1 = learning_rate * (target - op) * (1 - op) * op
    # n1 = learning_rate * (target - op)
    # print("n1 is "+str(n1))
    output_neuron.weight_vector = output_neuron.weight_vector + (n1 * hj_array)
    # printOutput(output_neuron, 0)

    # calculating the weights of the hidden nodes.
    number = len(hidden_neuron)
    for i in range(number):
        # sigmoidal output for hidden nodes.
        ho = hidden_neuron[i].output
        delta = n1 * output_neuron.weight_vector[i] * (1 - ho) * ho
        # delta = n1 * output_neuron.weight_vector[i]
        hidden_neuron[i].weight_vector = hidden_neuron[i].weight_vector + (delta * feature)

def train_network(feature, target, hidden_neuron, output_neuron):
    """ Make a forward pass, if output is not correct then make a back prop.
    """
    total = len(feature)
    # randomly iterating through the input vector.
    for i in random.sample(range(total), total):
        hj_array = forward_pass(feature[i,:], hidden_neuron, output_neuron)
        op = output_neuron.output
        # if output and target dont match, do back propogation.
        if float(round(decimal.Decimal(op), 1)) != target[i]:
            back_propogation(feature[i,:], hidden_neuron, output_neuron, hj_array, target[i])
    writeHiddenOp(hidden_neuron, 0,"a")
    writeHiddenOp(hidden_neuron, 1,"a")
    writeOutput(output_neuron, 0, "a")
    writeOutput(output_neuron, 1, "a")

def error_rate(feature, hidden_neuron, output_neuron, target):
    """ Calculating the error rate using the error function 1 - mismatch, 0 - match.
    """
    num = len(feature)
    misCalculated = 0
    for i in range(num):
        h_output = []
        # appended with 1 to deal with the bias for the output node.
        h_output.append(1)
        # calculating all the hjs - hidden output.
        for h in hidden_neuron:
            h.output = np.sum(feature[i,:] * h.weight_vector)
            # adding the output of hidden nodes to list.
            h_output.append(activation_function(h.output))

        hj_array = np.array(h_output, dtype=float)

        # calculating the output.
        output_neuron.output = np.sum(hj_array * output_neuron.weight_vector)
        op = float(round(activation_function(output_neuron.output), 1))
        if op != target[i]:
            misCalculated = misCalculated + 1
    # calculating the error rate.
    print("Total error rate is "+str(misCalculated/num))
    return (misCalculated/num)

# reading the input feature file.
def readCSV(textFile):
    """ Unpacking the CSV file into lists.
    """
    feature_vector = []
    target = []
    _output_dict = {"+":1.0, "-":0.0}
    with open(textFile, "r") as text:
        for line in text:
            textlist = line.rstrip().split(',')
            floatList = []
            floatList.append(1)
            for i in range(2):
                floatList.append(textlist[i])
            target.append(_output_dict[textlist[2]])
            feature_vector.append(floatList)
    return np.array(feature_vector, dtype=float), np.array(target, dtype=float)

# printing weight and output of hidden neurons.
def printHiddenOp(hidden_node, mode):
    """ 0-> weights, 1-> hj
    """
    for item in hidden_neuron:
        print("Hidden Neuron - "+item.id,end=" ")
        if mode == 0:
            print("weights-> ", end="")
            for i in range(3):
                print(item.weight_vector[i], end=",")
            print(" ")
        elif mode == 1:
            print("Output: "+str(item.output))

def writeHiddenOp(hidden_node, mode, wmode):
    """ 0-> weights, 1-> hj
    """
    output = ""
    with open("output.txt",wmode) as woutput:
        for item in hidden_neuron:
            output = "Hidden Neuron - " + item.id + " "
            if mode == 0:
                output = output + "weights-> "
                for i in range(3):
                    output = output + str(item.weight_vector[i]) + ","
            elif mode == 1:
                output = output + "Output: " + str(item.output)
            output = output + "\n"
            woutput.write(output)

def printOutput(output, mode):
    if mode == 0:
        print("Output Neuron Weight-> ",end="")
        for i in range(11):
            print(output.weight_vector[i], end=",")
        print("")
    elif mode == 1:
        print("Output Neuron :"+str(output.output))

def writeOutput(output_node, mode, wmode):
    output = ""
    with open("output.txt", wmode) as woutput:
        if mode == 0:
            output = "Output Neuron Weight-> "
            for i in range(11):
                output = output + str(output_node.weight_vector[i]) + ","
        elif mode == 1:
            output = "Output Neuron :" + str(output_node.output)
        output = output + "\n"
        woutput.write(output)

def writeError(output):
    with open("output.txt", "a") as woutput:
        output = output + "\n"
        woutput.write(output)

# start.
np.seterr(all='raise')
# setting decimal parameters.
c = decimal.getcontext()
c.prec = 8
c.rounding = decimal.ROUND_UP
# reading feature and target from the input file.
feature, target = readCSV("input.csv")
input_list = [1,2]

count = 
word, wordArray =

# creating a list of ten hidden nodes.
# hlist = []
# for i in range(10):
#     hlist.append(HiddenNeuron(i))
# hidden_neuron = np.array(hlist)
#
# # testing hidden neuron initializations.
# writeHiddenOp(hidden_neuron, 0,"w")
#
# # creating one output neuron.
# output_neuron = OutputNeuron()
# writeOutput(output_neuron, 0,"w")
#
# # train the network.
# epoch = 0
# min_error = 1
# while epoch < 100:
#     train_network(feature, target, hidden_neuron, output_neuron)
#     # error_rate(feature, hidden_neuron, output_neuron, target)
#     error = error_rate(feature_test, hidden_neuron, output_neuron, target_test)
#     if min_error > error:
#         min_error = error
#     writeError("Total error is "+str(error))
#     # print(" ")
#     epoch = epoch + 1
#
# print("Minimum error is "+str(min_error))
