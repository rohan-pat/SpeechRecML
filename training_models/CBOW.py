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
        self.h_output = None
        self.h_input = None

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

    def generateInputVector(self):
        text_list = sorted(self.text_set)
        count = 0
        for i in text_list:
            self.text_dict[i] = count
            count = count + 1
        for i in range(8):
            self.text_list.insert(i, "</s>")
            self.text_list.append("</s>")

    def forwardProp(self):
        total = 0;
        print("length of text list is "+str(len(self.text_list)))
        print(self.text_list[4-4:4+5])
        print(self.text_list[57116-4:57116+5])
        for i in range(4, len(self.text_list)):
            text_temp = self.text_list[i-4:i+5]
            if len(text_temp) != 9:
                break
            total = total + 1

            # create list of lists to create a C X V matrix
            inner_matrix = np.matrix(np.zeros((self.window_size, self.v), dtype=float))
            count = 0
            for item in text_temp:
                inner_matrix[count, self.text_dict[item]] = 1
                count = count + 1
            sum_matrix = np.sum(inner_matrix, axis=0)
            sum_matrix = sum_matrix / self.window_size
            self.h_output = np.dot(sum_matrix, self.w0)
            self.h_input = np.dot(self.h_output, self.w1)
            # calculate the exponential function for all the rows here.
            # print(self.h_input.shape)
            # then check how is the number represented utimately.
        print("Total is "+str(total))

if __name__ == "__main__":
    c = CBOW()
    c.loadText()
    c.generateInputVector()
    c.forwardProp()
