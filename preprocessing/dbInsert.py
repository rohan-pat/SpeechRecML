from pymongo import MongoClient
import json

class DBOperation:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.test #client['test']
        self.coll = self.db['speechRec'] #db.speechRec

    def insertFeatureData(self, key, word, wavArr, featureArr):
        data = {}
        data['word'] = word
        data['keyId'] = key
        data['wavArr'] = wavArr
        for i in range(len(featureArr)):
            data['feature'+str(i)] = featureArr[i]
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
