from pymongo import MongoClient
import json

client = MongoClient()
db = client.test #client['test']
coll = db['speechRec'] #db.speechRec

print("Db Insert")

print(db)

def processData():
    doc = {}
    someText = "I LOVE CHICKEN"
    keyId = 832562621
    sampleI = [34,16,676]
    sampleLove = [41,28,303,15]
    sampleChi = [24,355,573]
    wordArr = []
    wordArr.append({'word' : "I", 'wav_Array' : sampleI})
    wordArr.append({'word' : "LOVE", 'wav_Array' : sampleLove})
    wordArr.append({'word' : "CHICKEN", 'wav_Array' : sampleChi})
    #print(wordArr)
    doc['text'] = someText
    doc['keyId'] = keyId
    doc['wordArr'] = wordArr
    #jsonData = json.dumps(doc)
    return doc
    #return jsonData


jsonDoc = processData()
print(jsonDoc)

result = db.speechRec.insert_one(jsonDoc)
print(result)
