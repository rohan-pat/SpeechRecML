from pymongo import MongoClient
import json
import numpy as np

class DBOperation:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test #client['test']
        self.coll = self.db['speechRec'] #db.speechRec

    def getCount(self):
        count = self.db.inputFeatures.count()
        return count

    def getFeatures(self, num):
        data = self.db.inputFeatures.find()[num]
        finalData = []
        for i in data['featureArr']:
            wordData = []
            featureData = [item for sublist in i['features'] for item in sublist]
            wordData.append(i['word'])
            wordData.append(featureData)
            finalData.append(wordData)
        return finalData

    def storeWeightMatrix(self, weightMatrix):
        weightList = weightMatrix.tolist()
        data = {}
        data['weightList'] = weightList
        self.db.weights.remove({})
        self.db.weights.insert_one(data)

    def getWeightMatrix(self):
        data = self.db.weights.find()[0]
        weightMatrix = np.matrix(data['weightList'])
        return weightMatrix

    def insertFeatureData(self, key, text, featureList):
        data = {}
        words = text.split(" ")
        featureArr = []
        for i in range(len(words)):
            featureArr.append({'word' : words[i], 'features' : featureList[i]})

        data['text'] = text
        data['keyId'] = key
        data['featureArr'] = featureArr
        self.db.inputFeatures.insert_one(data)

    def insertRawData(self, keyId, text, sample):
        data = {}
        words = text.split(" ")
        wordArr = []
        for i in range(len(words)):
            wordArr.append({'word' : words[i], 'wav_Array' : sample[i]})

        data['text'] = text
        data['keyId'] = keyId
        data['wordArr'] = wordArr
        # print(data)
        self.db.inputData.insert_one(data)

if __name__ == "__main__":
    sample = [];
    sampleI = [34,16,676]
    sampleLove = [41,28,303,15]
    sampleChi = [24,355,573]
    sample.append(sampleI)
    sample.append(sampleLove)
    sample.append(sampleChi)
    someText = "I LOVE CHICKEN"
    keyId = 832562621

    rawJson = insertRawData(keyId, someText, sample)

    featureJson = insertFeatureData(keyId, "Rohan", sampleI, sample)

    # print(jsonDoc)
    print(featureJson)

    #result = db.speechRec.insert_one(jsonDoc)
    #print(result)
