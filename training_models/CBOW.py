""" Training continous bag of words model."""

import numpy as np
from nltk.stem.porter import PorterStemmer
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
        self.n = 50
        self.w0 = None
        self.text_dict = {}
        self.text_list = []
        self.window_size = 9
        # hidden_layer is the hidden layer.
        self.hidden_layer = None
        # output_layer is the output of the hidden layer.
        self.output_layer = None
        self.yj = None

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
        self.w0 = np.random.rand(self.v, self.n)
        self.w1 = np.random.rand(self.n, self.v)
        self.output_layer = np.matrix(np.random.rand(1, self.v))
        self.yj = np.matrix(np.random.rand(1, self.v))

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
        first = True
        print("length of text list is "+str(len(self.text_list)))
        for i in range(4, len(self.text_list)):
            text_temp = self.text_list[i-4:i+5]
            if len(text_temp) != 9:
                break
            total = total + 1

            # create list of lists to create a C X V matrix
            inner_matrix = np.matrix(np.zeros((self.window_size, self.v), dtype=float))
            count = 0
            index = self.text_dict[self.text_list[i]]
            for item in text_temp:
                inner_matrix[count, index] = 1
                count = count + 1
            sum_matrix = np.sum(inner_matrix, axis=0)
            sum_matrix = sum_matrix / self.window_size
            self.hidden_layer = np.dot(sum_matrix, self.w0)
            for j in range(self.v):
                uj = np.dot(self.hidden_layer, self.w1[:,[j]])
                # print(uj)
                self.output_layer[0, j] = activation_function(uj[0, 0])
            sum_exp = np.sum(self.output_layer, axis=1)
            # print("Shape of sum_exp = "+str(sum_exp.shape))
            for j in range(self.v):
                self.yj[0, j] = self.output_layer[0, j] / sum_exp[0,0]
            # then check how is the number represented utimately.
        print("Total is "+str(total))

if __name__ == "__main__":
    c = CBOW()
    c.loadText()
    c.generateInputVector()
    c.forwardProp()
