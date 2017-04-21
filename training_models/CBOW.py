""" Training continous bag of words model."""
import time
import numpy as np
from nltk.stem.porter import PorterStemmer
import sys
sys.path.insert(0, '/Users/Rohan/Documents/Studies/Spring2017/ML/ProjectCode/SpeechRecML/preprocessing')
from dbInsert import DBOperation
import decimal

def activation_function(x):
    # exponential function as activation
    # using decimal to better handle floating point underflow.
    x = decimal.Decimal(-x)
    z = x.exp()
    return float(round(decimal.Decimal(1) / decimal.Decimal(1 + z), 8))

class CBOW:
    def __init__(self):
        self.text = "bag-of-words.txt"
        # generating a set of unique words.
        self.text_set = None
        self.v = 0
        self.n = 10
        self.w0 = None
        self.text_dict = {}
        self.text_list = []
        self.window_size = 9
        # hidden_layer is the hidden layer.
        self.hidden_layer = None
        # output_layer is the output of the hidden layer.
        self.output_layer = None
        self.yj = None
        self.tj = None
        self.sum_exp = None
        self.uj_output = None

    def calculate_exp(self, uj_output):
        uj_list = []
        # print(uj_output.shape)
        for i in range(self.v):
            # print(uj_output[0, i])
            uj_list.append(activation_function(uj_output[0, i]))
        return np.matrix(uj_list)

    def loadText(self):
        with open(self.text, "r") as ftext:
            text = ftext.readlines()
            if len(text) != 1:
                print("Error Occured in reading dataset!")
            # stemming words to normalize them.
            text_list_temp = text[0].split(" ")
            st = PorterStemmer()
            for item in text_list_temp:
                self.text_list.append(st.stem((item)))
            self.text_set = set(self.text_list)
            print("size of text is "+str(len(self.text_set)))
            self.v = len(self.text_set)
        print("length of text list is "+str(len(self.text_list)))
        self.w0 = np.random.rand(self.v, self.n)
        self.w1 = np.random.rand(self.n, self.v)
        self.output_layer = np.matrix(np.random.rand(1, self.v))
        self.yj = np.matrix(np.random.rand(1, self.v))
        self.tj = np.matrix(np.random.rand(1, self.v))

    def generateInputVector(self):
        text_list = sorted(self.text_set)
        count = 0
        for i in text_list:
            self.text_dict[i] = count
            count = count + 1
        for i in range(4):
            self.text_list.insert(i, "</s>")
            self.text_list.append("</s>")

    def forwardProp(self):
        total = 0
        rcount = 0
        # print("length of text list is "+str(len(self.text_list)))
        for i in range(4, len(self.text_list)):
            text_temp = self.text_list[i-4:i+5]
            if len(text_temp) != 9:
                break
            total = total + 1

            inner_matrix = np.matrix(np.zeros((self.window_size, self.v), dtype=float))
            count = 0
            index = self.text_dict[self.text_list[i]]
            for item in text_temp:
                inner_matrix[count, index] = 1
                count = count + 1
            sum_matrix = np.sum(inner_matrix, axis=0)
            sum_matrix = sum_matrix / self.window_size
            self.hidden_layer = np.dot(sum_matrix, self.w0)
            output_list = []
            for j in range(self.v):
                rcount = rcount + 1
                uj = np.dot(self.hidden_layer, self.w1[:,[j]])
                # print(uj)
                output_list.append(uj[0, 0])
            self.uj_output = np.around(np.matrix(output_list), decimals=5)
            # print(self.uj_output.shape)
            # self.output_layer = self.calculate_exp(self.uj_output)
            self.output_layer = np.exp(self.uj_output)
            self.sum_exp = np.sum(self.output_layer, axis=1)
            # print("Shape of sum_exp = "+str(self.sum_exp.shape))
            self.yj = self.output_layer / self.sum_exp
        #     if total % 500 == 0:
        #         print("Count is "+str(rcount)+" ,"+str(total))
        # print("Total is "+str(total))

    def backPropogation(self):
        total = 0
        rcount = 0
        learning_rate = 0.3
        # print("length of text list is "+str(len(self.text_list)))
        # for i in range(4, len(self.text_list)):
        #     text_temp = self.text_list[i-4:i+5]
        #     if len(text_temp) != 9:
        #         break
        # total = total + 1
        # index = self.text_dict[self.text_list[i]]

        for i in range(self.v):
            self.tj = np.zeros((self.yj.shape), dtype=float)
            self.tj[0,i] = 1
            rcount = rcount + 1
            gradient1 = learning_rate * (self.yj[0,i] - self.tj[0,i]) * self.hidden_layer
            self.w1[:,[i]] = self.w1[:,[i]] - gradient1.transpose()

        gradient = (1 / self.window_size) * learning_rate
        EH = self.yj - self.tj
        EH = np.multiply(EH, self.w1)
        # print(EH.shape)
        self.w0 = self.w0 - EH.transpose()
        # if total % 500 == 0:
        #     print("Count is "+str(rcount)+" ,"+str(total))

    def calculateError(self):
        total_error = 0.0
        # print(self.uj_output.shape)
        for i in range(self.v):
            total_error = total_error - self.uj_output[0,i] - np.log(self.sum_exp)
        print("Total Error is "+str(total_error))
        return total_error

if __name__ == "__main__":
    c = CBOW()
    c.loadText()
    c.generateInputVector()
    epoch = 1
    total_error = 0
    total_runtime = time.time()
    d = DBOperation()
    while epoch != 100:
        print("---------%s-----------" %(epoch))
        f_time = time.time()
        c.forwardProp()
        print("Forward Prop => %s seconds" % round((time.time() - f_time), 2))

        b_time = time.time()
        c.backPropogation()
        print("Back Prop => %s seconds" % round((time.time() - b_time), 2))

        if total_error < c.calculateError():
            print("Lower error rate found")
            d.storeWeightMatrix(self.w0)

        epoch = epoch + 1
    print("Total time => %s seconds" % round((time.time() - total_runtime), 2))
